# CLI工具使用指南

## 概述

Sunbay提供了一套CLI工具，用于简化钉钉配置和管理。

## 安装

```bash
pip install -e .
```

安装后可使用以下命令：
- `sunbay-cli` - CLI工具入口
- `sunbay-server` - 启动服务

## 命令列表

### 1. 初始化配置

交互式配置钉钉应用信息：

```bash
sunbay-cli init
```

或直接运行：

```bash
python -m sunbay_official.cli.init_config
```

**配置项：**
- AppKey / AppSecret - 钉钉应用凭证
- CorpId - 企业ID
- Notable表格 - 支持URL自动解析或手动输入
- Operator ID - 操作者unionId
- 服务配置 - 监听地址和端口

**Notable URL解析示例：**

输入：
```
https://docs.dingtalk.com/i/nodes/vNG4YZ7JnPNd50RrIqDaoNk3W2LD0oRE?iframeQuery=sheetId%3DhERWDMS
```

自动解析为：
- Base ID: `vNG4YZ7JnPNd50RrIqDaoNk3W2LD0oRE`
- Sheet ID: `hERWDMS`

### 2. 解析Notable URL

快速解析Notable表格URL，提取配置参数：

```bash
sunbay-cli parse-notable <url>
```

或直接运行：

```bash
python -m sunbay_official.cli.parse_notable
```

**使用方式：**

方式1 - 命令行参数：
```bash
sunbay-cli parse-notable "https://docs.dingtalk.com/i/nodes/vNG4YZ7J?sheetId=hERWDMS"
```

方式2 - 交互式输入：
```bash
sunbay-cli parse-notable
# 然后输入URL
```

**示例输出：**

```bash
$ sunbay-cli parse-notable "https://docs.dingtalk.com/i/nodes/vNG4YZ7J?sheetId=hERWDMS"

======================================================================
Notable表格URL解析
======================================================================

======================================================================
✅ 解析成功！
======================================================================

Base ID (DINGTALK_SHEET_ID):  vNG4YZ7J
Sheet ID (DINGTALK_TABLE_ID): hERWDMS

======================================================================
配置到.env文件:
======================================================================
DINGTALK_SHEET_ID=vNG4YZ7J
DINGTALK_TABLE_ID=hERWDMS
======================================================================
```

**支持的URL格式：**

1. 标准格式：
   ```
   https://docs.dingtalk.com/i/nodes/{base_id}?sheetId={sheet_id}
   ```

2. iframe格式：
   ```
   https://docs.dingtalk.com/i/nodes/{base_id}?iframeQuery=sheetId%3D{sheet_id}
   ```

### 3. 获取UnionID

获取钉钉用户的unionId（用于operatorId配置）：

```bash
sunbay-cli get-unionid
```

或直接运行：

```bash
python -m sunbay_official.cli.get_unionid
```

**使用流程：**

1. 输入搜索关键词（姓名/手机号）
2. 从搜索结果中选择用户
3. 自动显示unionId
4. 可选：自动更新到.env配置

**示例：**

```bash
$ sunbay-cli get-unionid
请输入搜索关键词（姓名/手机号，留空搜索所有）: 王雷

正在获取access_token...
✅ Token获取成功

正在搜索用户: 王雷...
✅ 找到 1 个用户

======================================================================
1. 王雷@Bryan
   UserId: 0213473713-262887550
   UnionId: n9v6UniiYZ7Nv40tAgpZLpwiEiE
   手机: 13982085056

======================================================================

自动选择唯一用户: 王雷@Bryan

======================================================================
✅ 获取成功！
======================================================================
姓名: 王雷@Bryan
UnionId: n9v6UniiYZ7Nv40tAgpZLpwiEiE

是否更新到.env配置? (y/n) [y]: y
✅ 配置已更新
```

### 4. 启动服务

```bash
sunbay-cli server
```

或使用专用命令：

```bash
sunbay-server
```

## 完整工作流程

### 首次配置

```bash
# 1. 初始化配置
sunbay-cli init

# 2. 获取unionId（如果init时未配置）
sunbay-cli get-unionid

# 3. 启动服务
sunbay-server
```

### 配置文件

所有配置保存在项目根目录的 `.env` 文件：

```bash
# 钉钉配置
DINGTALK_APP_KEY=your_app_key
DINGTALK_APP_SECRET=your_app_secret
DINGTALK_CORP_ID=your_corp_id
DINGTALK_SHEET_ID=your_base_id
DINGTALK_TABLE_ID=your_sheet_id
DINGTALK_OPERATOR_ID=your_union_id

# 服务配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## 工具设计

### 模块结构

```
sunbay_official/cli/
├── __init__.py          # 模块初始化
├── main.py              # CLI统一入口
├── init_config.py       # 配置初始化工具
└── get_unionid.py       # UnionID获取工具
```

### 设计原则

1. **函数式风格** - 使用纯函数，避免类
2. **独立模块** - 每个工具独立可运行
3. **交互友好** - 清晰的提示和错误信息
4. **自动化** - URL解析、配置更新等自动处理
5. **可扩展** - 易于添加新工具

### 核心函数

#### init_config.py

- `parse_notable_url(url)` - 解析Notable URL
- `read_env()` - 读取.env配置
- `write_env(config)` - 写入.env配置
- `prompt(message, default)` - 交互式输入
- `init_config()` - 主流程

#### get_unionid.py

- `load_env()` - 加载.env配置
- `get_access_token_v1(app_key, app_secret)` - 获取token
- `search_users(access_token, keyword)` - 搜索用户
- `get_user_detail(access_token, user_id)` - 获取用户详情
- `update_env_operator_id(union_id)` - 更新配置
- `main()` - 主流程

## 扩展新工具

添加新CLI工具只需3步：

### 1. 创建工具文件

```python
# sunbay_official/cli/my_tool.py

def my_function():
    """工具函数"""
    pass

def main():
    """主入口"""
    print("我的工具")
    my_function()

if __name__ == '__main__':
    main()
```

### 2. 注册到CLI入口

```python
# sunbay_official/cli/main.py

elif command == 'my-tool':
    from sunbay_official.cli.my_tool import main as my_tool_main
    my_tool_main()
```

### 3. 更新帮助信息

```python
# sunbay_official/cli/main.py

def show_help():
    print("""
命令:
  ...
  my-tool     我的工具描述
""")
```

## 常见问题

### Q: URL解析失败怎么办？

A: 可以选择手动输入Base ID和Sheet ID，或检查URL格式是否正确。

### Q: 找不到用户怎么办？

A: 确保：
1. AppKey/AppSecret配置正确
2. 应用有通讯录读取权限
3. 搜索关键词正确

### Q: 配置更新不生效？

A: 重启服务后配置才会生效：
```bash
pkill -f sunbay
sunbay-server
```

## 技术细节

### Notable URL格式

支持两种格式：

1. **标准格式**：
   ```
   https://docs.dingtalk.com/i/nodes/{base_id}?sheetId={sheet_id}
   ```

2. **iframe格式**：
   ```
   https://docs.dingtalk.com/i/nodes/{base_id}?iframeQuery=sheetId%3D{sheet_id}
   ```

### UnionID vs UserID

- **UserID**: 企业内唯一ID，格式如 `0213473713-262887550`
- **UnionID**: 跨企业唯一ID，格式如 `n9v6UniiYZ7Nv40tAgpZLpwiEiE`

Notable API的operatorId参数需要使用UnionID。

### API版本

- 配置工具使用 **v2 API** (旧版gettoken)
- 服务运行使用 **新版OAuth2 API** (GetToken)

两者token不通用，但都能正常工作。
