"""
获取钉钉unionId的CLI工具
"""
import os
import sys
import requests
from pathlib import Path


def load_env():
    """加载.env配置"""
    env_path = Path.cwd() / '.env'
    config = {}
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config


def get_access_token_v1(app_key: str, app_secret: str) -> str:
    """获取旧版access_token (用于 topapi/v2/user/get)"""
    url = "https://oapi.dingtalk.com/gettoken"
    response = requests.get(url, params={"appkey": app_key, "appsecret": app_secret})
    result = response.json()
    if result.get("errcode") == 0:
        return result.get("access_token")
    raise Exception(f"获取token失败: {result.get('errmsg')}")


def get_access_token_v2(app_key: str, app_secret: str, corp_id: str) -> str:
    """获取新版access_token (用于 contact_1_0 SDK)"""
    from alibabacloud_dingtalk.oauth2_1_0 import client as oauth_client, models as oauth_models
    from alibabacloud_tea_openapi import models as open_api_models

    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'

    oauth = oauth_client.Client(config)
    request = oauth_models.GetTokenRequest(
        grant_type='client_credentials',
        client_id=app_key,
        client_secret=app_secret
    )
    response = oauth.get_token(corp_id, request)
    return response.body.access_token


def search_users(access_token: str, keyword: str) -> list:
    """
    搜索用户，返回userId列表
    使用 contact_1_0 SDK 的 search_user API
    """
    from alibabacloud_dingtalk.contact_1_0 import client as contact_client, models as contact_models
    from alibabacloud_tea_openapi import models as open_api_models
    from alibabacloud_tea_util import models as util_models

    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'

    c = contact_client.Client(config)

    request = contact_models.SearchUserRequest(
        query_word=keyword,
        offset=0,
        size=20
    )
    headers = contact_models.SearchUserHeaders()
    headers.x_acs_dingtalk_access_token = access_token

    response = c.search_user_with_options(request, headers, util_models.RuntimeOptions())

    if response and response.body:
        return response.body.to_map().get('list', [])

    return []


def get_user_detail(access_token: str, user_id: str) -> dict:
    """
    获取用户详情（包含unionId）
    
    Args:
        access_token: 访问令牌
        user_id: 用户ID
        
    Returns:
        用户详情字典
    """
    url = f"https://oapi.dingtalk.com/topapi/v2/user/get?access_token={access_token}"
    data = {"userid": user_id}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("result", {})
    
    return {}


def update_env_operator_id(union_id: str):
    """更新.env中的OPERATOR_ID"""
    env_path = Path.cwd() / '.env'
    
    if not env_path.exists():
        print("❌ .env文件不存在")
        return False
    
    lines = []
    updated = False
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('DINGTALK_OPERATOR_ID='):
                lines.append(f'DINGTALK_OPERATOR_ID={union_id}\n')
                updated = True
            else:
                lines.append(line)
    
    if updated:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    
    return False


def main():
    """主函数"""
    print("="*70)
    print("获取钉钉UnionID")
    print("="*70)
    print()
    
    # 加载配置
    config = load_env()
    
    app_key = config.get('DINGTALK_APP_KEY')
    app_secret = config.get('DINGTALK_APP_SECRET')
    
    if not app_key or not app_secret:
        print("❌ 请先运行 'python -m sunbay_official.cli.init_config' 配置应用信息")
        sys.exit(1)
    
    # 获取搜索关键词
    keyword = input("请输入搜索关键词（用户姓名）: ").strip()
    if not keyword:
        print("❌ 关键词不能为空")
        sys.exit(1)
    
    try:
        corp_id = config.get('DINGTALK_CORP_ID')
        
        # search_user 使用新版token，get_user_detail 使用旧版token
        print("\n正在获取access_token...")
        token_v2 = get_access_token_v2(app_key, app_secret, corp_id)
        token_v1 = get_access_token_v1(app_key, app_secret)
        print("✅ Token获取成功")
        
        # search_user 用新版token，get_user_detail 用旧版token
        print(f"\n正在搜索用户: {keyword}...")
        user_ids = search_users(token_v2, keyword)
        
        if not user_ids:
            print("❌ 未找到用户")
            sys.exit(1)
        
        print(f"✅ 找到 {len(user_ids)} 个用户\n")
        
        # 获取用户详情（含unionId）
        users = []
        for user_id in user_ids[:10]:
            detail = get_user_detail(token_v1, user_id)
            if detail:
                users.append(detail)
        
        # 显示用户列表
        print("="*70)
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.get('name', 'N/A')}")
            print(f"   UserId: {user.get('userid', 'N/A')}")
            print(f"   UnionId: {user.get('unionid', 'N/A')}")
            if user.get('mobile'):
                print(f"   手机: {user['mobile']}")
            if user.get('email'):
                print(f"   邮箱: {user['email']}")
            print()
        
        print("="*70)
        
        # 选择用户
        if len(users) == 1:
            selected = users[0]
            print(f"自动选择唯一用户: {selected.get('name')}")
        else:
            choice = input(f"\n请选择用户 (1-{len(users)}): ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(users):
                    selected = users[idx]
                else:
                    print("❌ 无效选择")
                    sys.exit(1)
            except ValueError:
                print("❌ 无效输入")
                sys.exit(1)
        
        union_id = selected.get('unionid')
        
        if not union_id:
            print("❌ 该用户没有unionId")
            sys.exit(1)
        
        print()
        print("="*70)
        print("✅ 获取成功！")
        print("="*70)
        print(f"姓名: {selected.get('name')}")
        print(f"UnionId: {union_id}")
        print()
        
        # 询问是否更新配置
        update = input("是否更新到.env配置? (y/n) [y]: ").strip().lower()
        
        if update in ('', 'y', 'yes'):
            if update_env_operator_id(union_id):
                print("✅ 配置已更新")
            else:
                print("⚠️  自动更新失败，请手动添加到.env:")
                print(f"DINGTALK_OPERATOR_ID={union_id}")
        else:
            print("\n请手动添加到.env:")
            print(f"DINGTALK_OPERATOR_ID={union_id}")
        
        print()
        print("="*70)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
