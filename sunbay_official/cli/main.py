#!/usr/bin/env python3
"""
Sunbay CLI工具
"""
import sys


def show_help():
    """显示帮助信息"""
    print("""
Sunbay CLI工具

用法:
  sunbay-cli <command> [options]

命令:
  init          初始化钉钉配置（交互式）
  get-unionid   获取钉钉unionId
  parse-notable 解析Notable表格URL
  server        启动服务（等同于 sunbay-server）
  help          显示此帮助信息

示例:
  sunbay-cli init                          # 初始化配置
  sunbay-cli get-unionid                   # 获取unionId
  sunbay-cli parse-notable <url>           # 解析Notable URL
  sunbay-cli server                        # 启动服务

或直接使用Python模块:
  python -m sunbay_official.cli.init_config
  python -m sunbay_official.cli.get_unionid
  python -m sunbay_official.cli.parse_notable
""")


def main():
    """CLI入口"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        from sunbay_official.cli.init_config import init_config
        init_config()
    
    elif command == 'get-unionid':
        from sunbay_official.cli.get_unionid import main as get_unionid_main
        get_unionid_main()
    
    elif command == 'parse-notable':
        from sunbay_official.cli.parse_notable import main as parse_notable_main
        parse_notable_main()
    
    elif command == 'server':
        from sunbay_official.main import main as server_main
        server_main()
    
    elif command in ('help', '--help', '-h'):
        show_help()
    
    else:
        print(f"❌ 未知命令: {command}")
        print("运行 'sunbay-cli help' 查看帮助")
        sys.exit(1)


if __name__ == '__main__':
    main()
