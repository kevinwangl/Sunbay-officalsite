# Sunbay Official Site

Sunbay 官网联系表单服务，集成钉钉 Notable 智能表格，自动记录客户提交信息。

## 快速开始

```bash
pip install -e .
cp .env.example .env  # 填写配置
sunbay-server
```

访问 `http://localhost:10000/static/index.html`

## 配置

### 方式一：交互式向导

```bash
sunbay-cli init
```

### 方式二：手动编辑 `.env`

```env
DINGTALK_APP_KEY=
DINGTALK_APP_SECRET=
DINGTALK_CORP_ID=
DINGTALK_SHEET_ID=      # Notable base_id
DINGTALK_TABLE_ID=      # Notable sheet_id
DINGTALK_OPERATOR_ID=   # 操作者 unionId
SERVER_HOST=0.0.0.0
SERVER_PORT=10000
```

获取 `DINGTALK_OPERATOR_ID`：

```bash
sunbay-cli get-unionid   # 按姓名搜索，自动写入 .env
```

解析 Notable URL：

```bash
sunbay-cli parse-notable "https://alidocs.dingtalk.com/i/nodes/xxx?sheetId=yyy"
```

## 部署（Render）

1. 推代码到 GitHub
2. Render → New Web Service → 连接仓库
3. Build Command: `pip install -e .`，Start Command: `sunbay-server`
4. 填写 Environment Variables（`.env` 中的 `DINGTALK_*` 变量）

## API

详见 [API.md](./API.md)

## 项目结构

```
sunbay_official/
├── api/contact.py          # 表单提交 & 重复检查接口
├── cli/                    # CLI 工具
├── dingtalk/               # 钉钉 SDK 封装（notable_1_0）
├── models/contact.py       # 表单数据模型
├── services/contact_service.py
├── config.py
└── main.py
static/index.html           # 联系表单页面
```

## Notable 表格字段

| 字段 | 说明 |
|------|------|
| 姓名 | Full Name |
| 邮箱 | Email |
| 公司 | Company |
| 手机 | Phone（可选）|
| 留言 | Note（可选）|
| IP地址 | 自动获取 |
| 创建时间 | 自动记录 |
