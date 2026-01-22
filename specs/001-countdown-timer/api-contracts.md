# 🔌 REST API 合约设计 - Stage 1 (P2)

**项目**: 事件倒计时工具  
**阶段**: Stage 1 设计 (P2 API)  
**日期**: 2026-01-22  
**API 版本**: v1  
**基础 URL**: `https://api.countdown-timer.app/v1`

---

## 📋 API 总览

### 认证

所有请求需要在 Header 中包含认证令牌：
```
Authorization: Bearer <token>
```

### 通用响应格式

**成功 (2xx)**:
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2026-01-22T10:30:00Z"
}
```

**错误 (4xx/5xx)**:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "人类可读的错误消息",
    "details": { ... }
  },
  "timestamp": "2026-01-22T10:30:00Z"
}
```

---

## 👤 认证接口

### 1. 用户注册

```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "timezone": "Asia/Shanghai"
}
```

**响应 (201)**:
```json
{
  "status": "success",
  "data": {
    "user_id": 123,
    "username": "john_doe",
    "email": "john@example.com",
    "token": "eyJhbGc...",
    "created_at": "2026-01-22T10:30:00Z"
  }
}
```

**错误**:
- `400 Bad Request`: 用户名或邮箱已存在
- `422 Unprocessable Entity`: 数据验证失败

---

### 2. 用户登录

```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "user_id": 123,
    "token": "eyJhbGc...",
    "expires_in": 86400
  }
}
```

---

## 📅 事件接口

### 3. 创建事件

```http
POST /events
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "生日",
  "target_date": "2026-03-15"
}
```

**响应 (201)**:
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "生日",
    "target_date": "2026-03-15",
    "created_at": "2026-01-22T10:30:00Z",
    "status": "ACTIVE",
    "remaining_days": 52,
    "url": "/events/1"
  }
}
```

**错误**:
- `400 Bad Request`: 名称已存在或日期格式错误
  ```json
  {
    "status": "error",
    "error": {
      "code": "DUPLICATE_NAME",
      "message": "事件 '生日' 已存在",
      "details": { "name": "生日" }
    }
  }
  ```
- `401 Unauthorized`: 未认证
- `422 Unprocessable Entity`: 数据验证失败

---

### 4. 获取所有事件

```http
GET /events?status=ACTIVE&limit=10&offset=0
Authorization: Bearer <token>
```

**查询参数**:
| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `status` | string | 状态过滤 (ACTIVE/CURRENT/EXPIRED/DELETED) | 全部 |
| `limit` | int | 返回数量 | 20 |
| `offset` | int | 分页偏移 | 0 |

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "events": [
      {
        "id": 1,
        "name": "生日",
        "target_date": "2026-03-15",
        "created_at": "2026-01-22T10:30:00Z",
        "status": "ACTIVE",
        "remaining_days": 52
      },
      {
        "id": 2,
        "name": "假期",
        "target_date": "2026-02-01",
        "created_at": "2026-01-22T11:00:00Z",
        "status": "ACTIVE",
        "remaining_days": 10
      }
    ],
    "pagination": {
      "total": 2,
      "limit": 10,
      "offset": 0,
      "has_more": false
    }
  }
}
```

---

### 5. 获取单个事件

```http
GET /events/{event_id}
Authorization: Bearer <token>
```

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "生日",
    "target_date": "2026-03-15",
    "created_at": "2026-01-22T10:30:00Z",
    "updated_at": "2026-01-22T10:30:00Z",
    "status": "ACTIVE",
    "remaining_days": 52,
    "is_public": false
  }
}
```

**错误**:
- `404 Not Found`: 事件不存在

---

### 6. 更新事件

```http
PUT /events/{event_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "target_date": "2026-04-15"
}
```

**可更新字段**:
- `target_date`: 目标日期
- `is_public`: 是否公开 (P3)

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "生日",
    "target_date": "2026-04-15",
    "updated_at": "2026-01-22T10:35:00Z",
    "status": "ACTIVE",
    "remaining_days": 82
  }
}
```

---

### 7. 删除事件

```http
DELETE /events/{event_id}
Authorization: Bearer <token>
```

**响应 (204 No Content)**:
```
(空响应体)
```

**错误**:
- `404 Not Found`: 事件不存在
- `403 Forbidden`: 无权删除

---

## 📱 小卡片接口 (P2)

### 8. 添加小卡片

```http
POST /widgets
Authorization: Bearer <token>
Content-Type: application/json

{
  "event_id": 1,
  "device_id": "device-iphone-001",
  "device_type": "iOS"
}
```

**响应 (201)**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid-1234",
    "event_name": "生日",
    "device_id": "device-iphone-001",
    "display_text": "生日还有 52 天",
    "created_at": "2026-01-22T10:30:00Z"
  }
}
```

---

### 9. 同步小卡片

```http
POST /widgets/sync
Authorization: Bearer <token>
Content-Type: application/json

{
  "device_id": "device-iphone-001"
}
```

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "widgets": [
      {
        "id": "uuid-1",
        "event_name": "生日",
        "display_text": "生日还有 52 天",
        "last_updated_at": "2026-01-22T10:00:00Z"
      },
      {
        "id": "uuid-2",
        "event_name": "假期",
        "display_text": "假期还有 10 天",
        "last_updated_at": "2026-01-22T10:00:00Z"
      }
    ],
    "synced_at": "2026-01-22T10:35:00Z"
  }
}
```

---

### 10. 删除小卡片

```http
DELETE /widgets/{widget_id}
Authorization: Bearer <token>
```

**响应 (204 No Content)**:
```
(空响应体)
```

---

## 🔔 通知接口 (P3)

### 11. 创建通知规则

```http
POST /events/{event_id}/notifications
Authorization: Bearer <token>
Content-Type: application/json

{
  "days_before": 7,
  "notification_type": "PUSH"
}
```

**notification_type 选项**:
- `PUSH`: 推送通知
- `EMAIL`: 邮件通知
- `SMS`: 短信通知

**响应 (201)**:
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "event_id": 1,
    "days_before": 7,
    "notification_type": "PUSH",
    "is_enabled": true,
    "next_trigger_at": "2026-03-08T00:00:00Z"
  }
}
```

---

### 12. 获取通知规则

```http
GET /events/{event_id}/notifications
Authorization: Bearer <token>
```

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "notifications": [
      {
        "id": 1,
        "days_before": 7,
        "notification_type": "PUSH",
        "is_enabled": true,
        "next_trigger_at": "2026-03-08T00:00:00Z"
      },
      {
        "id": 2,
        "days_before": 3,
        "notification_type": "EMAIL",
        "is_enabled": true,
        "next_trigger_at": "2026-03-12T00:00:00Z"
      }
    ]
  }
}
```

---

### 13. 删除通知规则

```http
DELETE /events/{event_id}/notifications/{notification_id}
Authorization: Bearer <token>
```

**响应 (204 No Content)**:
```
(空响应体)
```

---

## 🔗 分享接口 (P3)

### 14. 创建分享链接

```http
POST /events/{event_id}/share
Authorization: Bearer <token>
Content-Type: application/json

{
  "expires_in_days": 30
}
```

**响应 (201)**:
```json
{
  "status": "success",
  "data": {
    "share_id": "share-abc123",
    "share_url": "https://countdown-timer.app/share/abc123",
    "share_token": "token_xyz789",
    "created_at": "2026-01-22T10:30:00Z",
    "expires_at": "2026-02-21T10:30:00Z"
  }
}
```

---

### 15. 访问分享事件 (公开，无需认证)

```http
GET /share/{share_token}
```

**响应 (200)**:
```json
{
  "status": "success",
  "data": {
    "event_name": "生日",
    "target_date": "2026-03-15",
    "remaining_days": 52,
    "shared_by": "john_doe",
    "shared_at": "2026-01-22T10:30:00Z"
  }
}
```

---

## ⚠️ 错误码参考

| 错误码 | HTTP 状态 | 说明 |
|--------|---------|------|
| `INVALID_CREDENTIALS` | 401 | 认证凭证无效 |
| `TOKEN_EXPIRED` | 401 | 令牌已过期 |
| `FORBIDDEN` | 403 | 无权访问 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `DUPLICATE_NAME` | 409 | 事件名称已存在 |
| `INVALID_DATE_FORMAT` | 422 | 日期格式错误 |
| `VALIDATION_ERROR` | 422 | 数据验证失败 |
| `INTERNAL_ERROR` | 500 | 服务器错误 |

---

## 🔄 HTTP 状态码

| 状态码 | 说明 | 场景 |
|--------|------|------|
| `200 OK` | 请求成功 | GET / PUT 成功 |
| `201 Created` | 资源已创建 | POST 成功 |
| `204 No Content` | 成功但无返回 | DELETE 成功 |
| `400 Bad Request` | 请求格式错误 | 缺少必填字段 |
| `401 Unauthorized` | 需要认证 | 无效令牌 |
| `403 Forbidden` | 无权访问 | 尝试删除他人事件 |
| `404 Not Found` | 资源不存在 | 事件不存在 |
| `409 Conflict` | 冲突 | 重名事件 |
| `422 Unprocessable` | 验证失败 | 日期格式错误 |
| `429 Too Many` | 请求过多 | 限流 |
| `500 Internal Error` | 服务器错误 | 未处理异常 |

---

## 🎯 速率限制 (Rate Limiting)

**限制规则**:
- 每个用户每分钟最多 60 个请求
- 每个用户每小时最多 1000 个请求
- 限流窗口: 滑动窗口

**响应头**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1674362400
```

**超过限制 (429)**:
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "请求过于频繁，请稍后再试",
    "retry_after": 30
  }
}
```

---

## 📊 API 性能要求

| 指标 | 目标 | 备注 |
|------|------|------|
| 响应时间 (p50) | < 100 ms | 一般请求 |
| 响应时间 (p95) | < 200 ms | 正常负载 |
| 响应时间 (p99) | < 500 ms | 峰值负载 |
| 可用性 | 99.9% | 全年目标 |
| 吞吐量 | 100+ req/s | 单个实例 |

---

## 🔒 安全要求

### 认证

- ✅ 使用 JWT 令牌
- ✅ 令牌过期时间: 24 小时
- ✅ 刷新令牌机制 (可选)

### 授权

- ✅ 用户只能访问自己的事件
- ✅ 用户只能删除自己的事件
- ✅ 分享事件通过 share_token 访问

### 数据保护

- ✅ 所有传输使用 HTTPS
- ✅ 密码使用 bcrypt 加密
- ✅ 敏感数据不在日志中

---

## 📚 API 文档工具

**推荐使用 Swagger/OpenAPI**:

```bash
# 使用 FastAPI 自动生成
pip install fastapi
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## ✅ 合约验收标准

**API 实现时**:
- [ ] 所有 15 个端点实现
- [ ] 所有错误情况覆盖
- [ ] 所有响应格式一致
- [ ] 认证/授权工作正常
- [ ] 限流机制有效
- [ ] 响应时间 < 200ms (p95)

---

**API 设计完成日期**: 2026-01-22  
**准备进入 Stage 2 (项目设置)**: ✅ 可开始

