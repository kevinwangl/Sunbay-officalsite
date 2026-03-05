# Sunbay Official Site

Sunbay官网联系表单系统，集成钉钉Notable智能表格。

## 安装

```bash
pip3 install -e .
```

## 配置

### 1. 初始化配置

```bash
sunbay-cli init
```

交互式向导，依次配置：
- 钉钉 AppKey / AppSecret / CorpId
- Notable 表格 URL（自动解析 base_id 和 sheet_id）
- Operator ID（自动搜索用户获取 unionId）

### 2. 单独获取 UnionId

```bash
sunbay-cli get-unionid
```

### 3. 单独解析 Notable URL

```bash
sunbay-cli parse-notable "https://alidocs.dingtalk.com/i/nodes/xxx?sheetId=yyy"
```

## 运行

```bash
sunbay-server
```

访问：
- 联系表单：http://localhost:8000/static/index.html
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 项目结构

```
sunbay_official/
├── api/            # FastAPI 路由
├── cli/            # CLI 工具
│   ├── main.py         # 入口
│   ├── init_config.py  # 初始化配置
│   ├── get_unionid.py  # 获取 unionId
│   └── parse_notable.py # 解析 Notable URL
├── dingtalk/       # 钉钉集成
│   ├── base.py         # 基础客户端
│   ├── sheet.py        # Notable 表格操作
│   └── exceptions.py   # 异常定义
├── models/         # 数据模型
├── services/       # 业务逻辑
├── config.py       # 配置管理
└── main.py         # 应用入口
static/
└── index.html      # 联系表单页面
```

## 环境变量

```bash
DINGTALK_APP_KEY=       # 应用 AppKey
DINGTALK_APP_SECRET=    # 应用 AppSecret
DINGTALK_CORP_ID=       # 企业 CorpId
DINGTALK_SHEET_ID=      # Notable base_id
DINGTALK_TABLE_ID=      # Notable sheet_id
DINGTALK_OPERATOR_ID=   # 操作者 unionId
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## 技术栈

- FastAPI + Uvicorn
- alibabacloud_dingtalk SDK (notable_1_0)
- pydantic-settings
