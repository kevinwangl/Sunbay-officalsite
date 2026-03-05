"""
解析Notable表格URL，提取配置参数
"""
import sys
import re
from urllib.parse import urlparse, parse_qs


def parse_notable_url(url: str) -> dict:
    """
    解析Notable表格URL，提取base_id和sheet_id
    
    Args:
        url: Notable表格完整URL
        
    Returns:
        包含base_id和sheet_id的字典
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


def main():
    """主函数"""
    print("="*70)
    print("Notable表格URL解析")
    print("="*70)
    print()
    
    # 获取URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("请输入Notable表格完整URL:")
        print("示例: https://docs.dingtalk.com/i/nodes/vNG4YZ7J?sheetId=hERWDMS")
        print()
        url = input("URL: ").strip()
    
    if not url:
        print("❌ URL不能为空")
        sys.exit(1)
    
    try:
        # 解析URL
        result = parse_notable_url(url)
        
        print()
        print("="*70)
        print("✅ 解析成功！")
        print("="*70)
        print()
        print(f"Base ID (DINGTALK_SHEET_ID):  {result['base_id']}")
        print(f"Sheet ID (DINGTALK_TABLE_ID): {result['sheet_id']}")
        print()
        print("="*70)
        print("配置到.env文件:")
        print("="*70)
        print(f"DINGTALK_SHEET_ID={result['base_id']}")
        print(f"DINGTALK_TABLE_ID={result['sheet_id']}")
        print("="*70)
        
    except ValueError as e:
        print()
        print(f"❌ 解析失败: {e}")
        print()
        print("支持的URL格式:")
        print("  1. https://docs.dingtalk.com/i/nodes/{base_id}?sheetId={sheet_id}")
        print("  2. https://docs.dingtalk.com/i/nodes/{base_id}?iframeQuery=sheetId%3D{sheet_id}")
        sys.exit(1)


if __name__ == '__main__':
    main()
