# CLI 工具指南

## 安装

```bash
pip install -e .
```

## 命令

### `sunbay-cli init`
交互式配置向导，设置钉钉应用凭证、Notable 表格、operatorId 等，自动写入 `.env`。

### `sunbay-cli get-unionid`
按姓名/手机号搜索钉钉用户，获取 unionId，可自动更新到 `.env`。

```bash
$ sunbay-cli get-unionid
请输入搜索关键词: 王雷
✅ 找到用户: 王雷  UnionId: n9v6UniiYZ7Nv40tAgpZLpwiEiE
是否更新到.env? (y/n): y
```

### `sunbay-cli parse-notable <url>`
从 Notable 表格 URL 中提取 `DINGTALK_SHEET_ID` 和 `DINGTALK_TABLE_ID`。

```bash
$ sunbay-cli parse-notable "https://alidocs.dingtalk.com/i/nodes/vNG4YZ7J?sheetId=hERWDMS"
DINGTALK_SHEET_ID=vNG4YZ7J
DINGTALK_TABLE_ID=hERWDMS
```

支持两种 URL 格式：
- `?sheetId=xxx`
- `?iframeQuery=...sheetId%3Dxxx`

### `sunbay-server`
启动 FastAPI 服务（默认端口 10000）。

## .env 配置项

```env
DINGTALK_APP_KEY=
DINGTALK_APP_SECRET=
DINGTALK_CORP_ID=
DINGTALK_SHEET_ID=      # Notable base_id
DINGTALK_TABLE_ID=      # Notable sheet_id（表格内的 sheet）
DINGTALK_OPERATOR_ID=   # 操作者 unionId
SERVER_HOST=0.0.0.0
SERVER_PORT=10000
```
