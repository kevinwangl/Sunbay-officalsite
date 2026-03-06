# API 接口文档

Base URL: `https://sunbay-officalsite.onrender.com`

---

## 1. 提交联系表单

**POST** `/api/contact`

### Request Body

```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "company": "示例公司",
  "phone": "13800138000",
  "message": "感兴趣的产品..."
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 姓名，最长 50 字符 |
| email | string | ✅ | 邮箱地址 |
| company | string | ✅ | 公司名称，最长 100 字符 |
| phone | string | ❌ | 电话号码，最长 20 字符 |
| message | string | ❌ | 留言内容，最长 500 字符 |

> IP 地址由服务端自动从请求中获取，无需前端传递。

### Response

**201 Created**
```json
{
  "success": true,
  "message": "提交成功",
  "data": {
    "record_id": { "id": "xxxxxxxx" }
  }
}
```

**422 Unprocessable Entity**（字段校验失败）
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "提交失败: ..."
}
```

---

## 2. 重复提交检查

**GET** `/api/contact/check`

### Query Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | string | ❌ | 邮箱（email / phone 至少传一个） |
| phone | string | ❌ | 电话 |

### Example

```
GET /api/contact/check?email=zhangsan@example.com
GET /api/contact/check?email=zhangsan@example.com&phone=13800138000
```

### Response

**200 OK**
```json
{ "duplicate": false }
```
```json
{ "duplicate": true }
```

**400 Bad Request**（未传任何参数）
```json
{ "detail": "请提供 phone 或 email 参数" }
```

---

## 前端集成示例

```javascript
// 1. 先检查是否重复
const checkRes = await fetch(`/api/contact/check?email=${encodeURIComponent(email)}`);
const { duplicate } = await checkRes.json();
if (duplicate) {
  alert('该邮箱已提交过');
  return;
}

// 2. 提交表单
const res = await fetch('/api/contact', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name, email, company, phone, message })
});
const result = await res.json();
```
