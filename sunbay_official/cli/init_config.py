"""
钉钉配置初始化CLI工具
用于交互式配置钉钉应用
"""
import os
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def parse_notable_url(url: str) -> dict:
    """
    解析Notable表格URL，提取base_id和sheet_id
    
    Args:
        url: Notable表格完整URL
        
    Returns:
        包含base_id和sheet_id的字典
        
    Example:
        >>> parse_notable_url("https://docs.dingtalk.com/i/nodes/vNG4YZ7J?sheetId=hERWDMS")
        {'base_id': 'vNG4YZ7J', 'sheet_id': 'hERWDMS'}
    """
    # 提取base_id (在/nodes/后面)
    base_id_match = re.search(r'/nodes/([^?&#]+)', url)
    if not base_id_match:
        raise ValueError("无法从URL中提取base_id")
    
    base_id = base_id_match.group(1)
    
    # 提取sheet_id (从查询参数中)
    parsed = urlparse(url)
    
    # 处理iframeQuery参数
    if 'iframeQuery' in parsed.query:
        query_params = parse_qs(parsed.query)
        iframe_query = query_params.get('iframeQuery', [''])[0]
        sheet_match = re.search(r'sheetId=([^&]+)', iframe_query)
        if sheet_match:
            return {
                'base_id': base_id,
                'sheet_id': sheet_match.group(1)
            }
    
    # 直接从查询参数提取
    query_params = parse_qs(parsed.query)
    sheet_id = query_params.get('sheetId', [None])[0]
    
    if not sheet_id:
        raise ValueError("无法从URL中提取sheet_id")
    
    return {
        'base_id': base_id,
        'sheet_id': sheet_id
    }


def get_env_path() -> Path:
    """获取.env文件路径"""
    return Path.cwd() / '.env'


def read_env() -> dict:
    """读取现有.env配置"""
    env_path = get_env_path()
    config = {}
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config


def write_env(config: dict):
    """写入.env配置"""
    env_path = get_env_path()
    
    lines = [
        "# 钉钉配置",
        f"DINGTALK_APP_KEY={config.get('DINGTALK_APP_KEY', '')}",
        f"DINGTALK_APP_SECRET={config.get('DINGTALK_APP_SECRET', '')}",
        f"DINGTALK_CORP_ID={config.get('DINGTALK_CORP_ID', '')}",
        f"DINGTALK_SHEET_ID={config.get('DINGTALK_SHEET_ID', '')}",
        f"DINGTALK_TABLE_ID={config.get('DINGTALK_TABLE_ID', '')}",
        f"DINGTALK_OPERATOR_ID={config.get('DINGTALK_OPERATOR_ID', '')}",
        "",
        "# 服务配置",
        f"SERVER_HOST={config.get('SERVER_HOST', '0.0.0.0')}",
        f"SERVER_PORT={config.get('SERVER_PORT', '8000')}",
        ""
    ]
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ 配置已保存到 {env_path}")


def prompt(message: str, default: str = None) -> str:
    """交互式输入提示"""
    if default:
        message = f"{message} [{default}]"
    
    value = input(f"{message}: ").strip()
    return value if value else default


def _fetch_operator_id(config: dict) -> str:
    """
    通过搜索用户获取operatorId (unionId)
    
    流程: 搜索关键词 → userId → v2/user/get → unionId
    """
    from .get_unionid import get_access_token_v1, search_users, get_user_detail
    
    print()
    print("需要获取操作者的 unionId 作为 operatorId")
    print("流程: 搜索用户 → 获取 userId → 转换为 unionId")
    print()
    
    keyword = input("请输入搜索关键词（用户姓名）: ").strip()
    if not keyword:
        print("⚠️  跳过，请稍后运行 'sunbay-cli get-unionid' 手动获取")
        return ''
    
    try:
        app_key = config.get('DINGTALK_APP_KEY')
        app_secret = config.get('DINGTALK_APP_SECRET')
        corp_id = config.get('DINGTALK_CORP_ID')
        
        if not app_key or not app_secret:
            print("❌ 请先配置 AppKey 和 AppSecret")
            return ''
        
        print("正在获取 access_token...")
        from .get_unionid import get_access_token_v1, get_access_token_v2, search_users, get_user_detail
        token_v2 = get_access_token_v2(app_key, app_secret, corp_id)
        token_v1 = get_access_token_v1(app_key, app_secret)
        
        print(f"正在搜索用户: {keyword}...")
        user_ids = search_users(token_v2, keyword)
        
        if not user_ids:
            print("❌ 未找到用户，请稍后运行 'sunbay-cli get-unionid' 手动获取")
            return ''
        
        # 获取用户详情
        users = []
        for user_id in user_ids[:10]:
            detail = get_user_detail(token_v1, user_id)
            if detail:
                users.append(detail)
        
        # 显示用户列表
        print()
        for i, user in enumerate(users, 1):
            print(f"  {i}. {user.get('name', 'N/A')} | userId: {user.get('userid')} | unionId: {user.get('unionid')}")
        print()
        
        # 选择用户
        if len(users) == 1:
            selected = users[0]
            print(f"自动选择: {selected.get('name')}")
        else:
            choice = input(f"请选择用户 (1-{len(users)}): ").strip()
            try:
                selected = users[int(choice) - 1]
            except (ValueError, IndexError):
                print("❌ 无效选择，请稍后手动配置")
                return ''
        
        union_id = selected.get('unionid', '')
        print(f"✅ 获取成功: {union_id}")
        return union_id
        
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        print("请稍后运行 'sunbay-cli get-unionid' 手动获取")
        return ''


def init_config():
    """交互式初始化配置"""
    print("="*70)
    print("钉钉配置初始化向导")
    print("="*70)
    print()
    
    # 读取现有配置
    existing = read_env()
    
    config = {}
    
    # 基础配置
    print("📋 基础配置")
    print("-"*70)
    config['DINGTALK_APP_KEY'] = prompt(
        "应用AppKey",
        existing.get('DINGTALK_APP_KEY')
    )
    config['DINGTALK_APP_SECRET'] = prompt(
        "应用AppSecret",
        existing.get('DINGTALK_APP_SECRET')
    )
    config['DINGTALK_CORP_ID'] = prompt(
        "企业CorpId",
        existing.get('DINGTALK_CORP_ID')
    )
    print()
    
    # Notable配置
    print("📊 Notable表格配置")
    print("-"*70)
    
    use_url = prompt("是否通过URL配置表格? (y/n)", "y").lower() == 'y'
    
    if use_url:
        url = prompt("请输入Notable表格完整URL")
        try:
            parsed = parse_notable_url(url)
            config['DINGTALK_SHEET_ID'] = parsed['base_id']
            config['DINGTALK_TABLE_ID'] = parsed['sheet_id']
            print(f"✅ 解析成功:")
            print(f"   Base ID: {parsed['base_id']}")
            print(f"   Sheet ID: {parsed['sheet_id']}")
        except ValueError as e:
            print(f"❌ URL解析失败: {e}")
            config['DINGTALK_SHEET_ID'] = prompt("请手动输入Base ID")
            config['DINGTALK_TABLE_ID'] = prompt("请手动输入Sheet ID")
    else:
        config['DINGTALK_SHEET_ID'] = prompt(
            "Base ID",
            existing.get('DINGTALK_SHEET_ID')
        )
        config['DINGTALK_TABLE_ID'] = prompt(
            "Sheet ID",
            existing.get('DINGTALK_TABLE_ID')
        )
    print()
    
    # Operator ID配置
    print("👤 操作者配置")
    print("-"*70)
    
    existing_operator_id = existing.get('DINGTALK_OPERATOR_ID')
    if existing_operator_id:
        print(f"当前 Operator ID: {existing_operator_id}")
        keep = prompt("是否保留? (y/n)", "y").lower()
        if keep == 'y':
            config['DINGTALK_OPERATOR_ID'] = existing_operator_id
        else:
            config['DINGTALK_OPERATOR_ID'] = _fetch_operator_id(config)
    else:
        config['DINGTALK_OPERATOR_ID'] = _fetch_operator_id(config)
    print()
    
    # 服务配置
    print("🚀 服务配置")
    print("-"*70)
    config['SERVER_HOST'] = prompt("监听地址", existing.get('SERVER_HOST', '0.0.0.0'))
    config['SERVER_PORT'] = prompt("监听端口", existing.get('SERVER_PORT', '8000'))
    print()
    
    # 保存配置
    write_env(config)
    
    print()
    print("="*70)
    print("✅ 配置完成！")
    print()
    print("下一步:")
    print("  1. 运行 'python -m sunbay_official.cli.get_unionid' 获取unionId (如未配置)")
    print("  2. 运行 'sunbay-server' 启动服务")
    print("="*70)


if __name__ == '__main__':
    init_config()
