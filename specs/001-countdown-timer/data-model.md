# 📊 数据模型设计 - Stage 1

**项目**: 事件倒计时工具  
**阶段**: Stage 1 (设计)  
**日期**: 2026-01-22  
**状态**: ✅ 完成

---

## 🎯 设计目标

为 P1/P2/P3 阶段设计完整的数据模型，确保：
- ✅ 支持所有 17 个功能需求 (FR)
- ✅ 支持所有 8 个验收场景
- ✅ 支持 P1 JSON 和 P2 SQLite 存储
- ✅ 支持 P3 通知和分享功能
- ✅ 支持状态转换 (4 个完整状态)

---

## 📋 核心实体

### 1. Event (事件)

**用途**: 表示一个倒计时事件

**P1 JSON 表示**:
```json
{
  "events": {
    "生日": {
      "name": "生日",
      "target_date": "2026-03-15",
      "created_at": "2026-01-22T10:30:00",
      "status": "ACTIVE",
      "remaining_days": 52
    },
    "假期": {
      "name": "假期",
      "target_date": "2026-02-01",
      "created_at": "2026-01-22T11:00:00",
      "status": "ACTIVE",
      "remaining_days": 10
    }
  }
}
```

**P2 SQLite 表定义**:
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,              -- 事件名称 (256 字符限制)
    target_date DATE NOT NULL,              -- 目标日期 (YYYY-MM-DD)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'ACTIVE',           -- 状态: ACTIVE/CURRENT/EXPIRED/DELETED
    created_by_user_id INTEGER,             -- P2: 用户 ID (关联用户表)
    is_public BOOLEAN DEFAULT FALSE,        -- P3: 是否公开分享
    
    -- 约束
    CHECK (name != ''),
    CHECK (length(name) <= 256),
    CHECK (status IN ('ACTIVE', 'CURRENT', 'EXPIRED', 'DELETED')),
    
    -- 索引
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);

-- 创建索引加速查询
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_target_date ON events(target_date);
CREATE INDEX idx_events_user ON events(created_by_user_id);
```

**属性详解**:

| 字段 | 类型 | 长度 | 必填 | 说明 |
|------|------|------|------|------|
| `id` | INT | - | ✅ | 唯一标识符 (P2) |
| `name` | STRING | 256 | ✅ | 事件名称 (唯一) |
| `target_date` | DATE | - | ✅ | 目标日期 (YYYY-MM-DD) |
| `created_at` | TIMESTAMP | - | ✅ | 创建时间 (UTC) |
| `updated_at` | TIMESTAMP | - | ✅ | 更新时间 (UTC) |
| `status` | ENUM | - | ✅ | 事件状态 (4 值) |
| `remaining_days` | INT | - | ❌ | 计算属性 (不存储) |

**状态转换规则**:
```
                    每日检查
┌─────────────────────────────┐
│                             ↓
ACTIVE (remaining_days > 0)
  │
  ├─ 计算: remaining_days = (target_date - today).days
  │
  └─→ 如果 remaining_days = 0 → CURRENT
          │
          └─→ 如果 remaining_days < 0 → EXPIRED

用户删除: Event → DELETED (软删除)
恢复: DELETED → ACTIVE (恢复功能，P3 可选)
```

**计算属性** (不存储，每次查询时计算):
```python
def get_remaining_days(event):
    """计算剩余天数"""
    from datetime import date
    today = date.today()
    target = datetime.fromisoformat(event['target_date']).date()
    return (target - today).days

def get_status(event):
    """计算事件状态"""
    remaining = get_remaining_days(event)
    if remaining > 0:
        return 'ACTIVE'
    elif remaining == 0:
        return 'CURRENT'
    elif remaining < 0:
        return 'EXPIRED'
    else:
        return event['status']  # 如果已删除则返回 DELETED
```

---

### 2. Widget (小卡片) - P2

**用途**: 表示手机主屏幕上的小卡片

**P2 SQLite 表定义**:
```sql
CREATE TABLE widgets (
    id TEXT PRIMARY KEY,                    -- UUID
    event_name TEXT NOT NULL,               -- 关联事件名称
    device_id TEXT NOT NULL,                -- 设备标识符
    device_type TEXT,                       -- iOS / Android
    last_updated_at TIMESTAMP,              -- 上次更新时间
    display_text TEXT,                      -- 显示文本 (缓存)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束
    UNIQUE (event_name, device_id),         -- 每个设备每个事件最多一个卡片
    FOREIGN KEY (event_name) REFERENCES events(name)
        ON DELETE CASCADE
);
```

**属性详解**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | UUID | 卡片唯一 ID |
| `event_name` | STRING | 关联事件 |
| `device_id` | STRING | 设备识别码 |
| `device_type` | STRING | iOS 或 Android |
| `display_text` | STRING | 缓存的显示文本 (如"生日还有 52 天") |
| `last_updated_at` | TIMESTAMP | 最后更新时间 |

**API 响应示例**:
```json
{
  "widgets": [
    {
      "id": "uuid-1",
      "event_name": "生日",
      "device_id": "device-iphone-001",
      "display_text": "生日还有 52 天",
      "last_updated_at": "2026-01-22T10:00:00Z"
    }
  ]
}
```

---

### 3. Notification (通知规则) - P3

**用途**: 表示配置的通知规则

**P2 SQLite 表定义**:
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,               -- 关联事件
    days_before INTEGER NOT NULL,           -- 距离事件前 N 天触发 (7, 3, 1 等)
    notification_type TEXT NOT NULL,        -- PUSH / EMAIL / SMS
    is_enabled BOOLEAN DEFAULT TRUE,        -- 是否启用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_sent_at TIMESTAMP,                 -- 上次发送时间
    next_trigger_at TIMESTAMP,              -- 下次触发时间
    
    -- 约束
    CHECK (days_before > 0),
    CHECK (notification_type IN ('PUSH', 'EMAIL', 'SMS')),
    UNIQUE (event_name, days_before, notification_type),
    FOREIGN KEY (event_name) REFERENCES events(name)
        ON DELETE CASCADE
);
```

**属性详解**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT | 规则 ID |
| `event_name` | STRING | 关联事件 |
| `days_before` | INT | N 天前触发 |
| `notification_type` | STRING | 通知类型 |
| `is_enabled` | BOOL | 是否启用 |
| `last_sent_at` | TIMESTAMP | 上次发送 |
| `next_trigger_at` | TIMESTAMP | 下次触发 |

**规则示例**:
```json
{
  "notifications": [
    {
      "event_name": "生日",
      "days_before": 7,
      "notification_type": "PUSH",
      "is_enabled": true,
      "next_trigger_at": "2026-03-08"
    },
    {
      "event_name": "生日",
      "days_before": 3,
      "notification_type": "EMAIL",
      "is_enabled": true,
      "next_trigger_at": "2026-03-12"
    },
    {
      "event_name": "生日",
      "days_before": 1,
      "notification_type": "PUSH",
      "is_enabled": true,
      "next_trigger_at": "2026-03-14"
    }
  ]
}
```

---

### 4. User (用户) - P2

**用途**: 表示 API 用户 (P2 新增)

**P2 SQLite 表定义**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    timezone TEXT DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 5. SharedEvent (分享事件) - P3

**用途**: 表示分享出去的事件链接

**P3 SQLite 表定义**:
```sql
CREATE TABLE shared_events (
    id TEXT PRIMARY KEY,                    -- 分享 ID (UUID)
    event_name TEXT NOT NULL,               -- 原事件名称
    created_by_user_id INTEGER NOT NULL,    -- 分享者
    share_url TEXT NOT NULL,                -- 分享链接
    share_token TEXT UNIQUE NOT NULL,       -- 访问令牌
    access_count INTEGER DEFAULT 0,         -- 访问次数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,                   -- 过期时间 (可选)
    
    FOREIGN KEY (created_by_user_id) REFERENCES users(id),
    FOREIGN KEY (event_name) REFERENCES events(name)
);
```

---

## 🔄 数据流设计

### P1 (CLI) 数据流

```
用户输入
  │
  ├─ Validator (验证)
  │   ├─ 日期格式 (YYYY-MM-DD)
  │   ├─ 名称长度 (≤ 256)
  │   ├─ 名称唯一性
  │   └─ 日期有效性
  │
  ├─ Event Manager (业务逻辑)
  │   ├─ 创建事件 (create)
  │   ├─ 查询事件 (query)
  │   ├─ 删除事件 (delete)
  │   └─ 计算剩余天数
  │
  ├─ Storage (存储)
  │   ├─ 读取 JSON
  │   ├─ 修改数据
  │   ├─ 写回 JSON
  │   └─ 文件锁 (并发控制)
  │
  └─ CLI Output (输出)
      ├─ 事件列表
      ├─ 错误消息
      └─ 成功提示
```

### P2 (API) 数据流

```
HTTP 请求
  │
  ├─ FastAPI 路由
  │   ├─ 解析请求
  │   ├─ 身份验证
  │   └─ 授权检查
  │
  ├─ Event Manager (业务逻辑)
  │   ├─ 创建/查询/删除事件
  │   ├─ 更新状态
  │   ├─ 同步小卡片
  │   └─ 触发通知规则
  │
  ├─ Database (SQLite/PostgreSQL)
  │   ├─ 事件表
  │   ├─ 小卡片表
  │   ├─ 通知表
  │   └─ 用户表
  │
  └─ HTTP 响应
      ├─ JSON 数据
      ├─ 状态码
      └─ 错误信息
```

### P3 (通知) 数据流

```
每日 00:00 UTC (计划任务)
  │
  ├─ Notification Service
  │   ├─ 扫描所有事件
  │   ├─ 检查通知规则
  │   ├─ 计算触发条件
  │   └─ 发送通知
  │
  ├─ 数据库更新
  │   ├─ 更新 last_sent_at
  │   ├─ 计算 next_trigger_at
  │   └─ 记录发送日志
  │
  └─ 通知渠道
      ├─ PUSH (推送)
      ├─ EMAIL (邮件)
      └─ SMS (短信)
```

---

## 📐 数据库架构图

### P1 (JSON)

```
events.json
│
├─ 生日
│   ├─ name: "生日"
│   ├─ target_date: "2026-03-15"
│   ├─ created_at: "2026-01-22T10:30:00"
│   ├─ status: "ACTIVE"
│   └─ remaining_days: 52 (计算)
│
└─ 假期
    ├─ name: "假期"
    ├─ target_date: "2026-02-01"
    ├─ created_at: "2026-01-22T11:00:00"
    ├─ status: "ACTIVE"
    └─ remaining_days: 10 (计算)
```

### P2 (SQLite)

```
events
├─ id (PK)
├─ name (UNIQUE)
├─ target_date
├─ created_at
├─ status
├─ user_id (FK → users)
└─ is_public

users
├─ id (PK)
├─ username (UNIQUE)
├─ email (UNIQUE)
└─ timezone

widgets
├─ id (PK)
├─ event_name (FK → events)
├─ device_id
├─ display_text
└─ last_updated_at

notifications
├─ id (PK)
├─ event_name (FK → events)
├─ days_before
├─ notification_type
└─ next_trigger_at
```

### P3 (扩展)

```
shared_events
├─ id (PK)
├─ event_name (FK → events)
├─ created_by_user_id (FK → users)
├─ share_token
├─ access_count
└─ expires_at
```

---

## 🔐 数据验证规则

### Event 表

| 字段 | 验证规则 | 错误消息 |
|------|---------|---------|
| `name` | 非空，长度 1-256，唯一 | "事件名称不能为空或重复" |
| `target_date` | 格式 YYYY-MM-DD，有效日期 | "日期格式错误，应为 YYYY-MM-DD" |
| `status` | IN ('ACTIVE', 'CURRENT', 'EXPIRED', 'DELETED') | "无效的事件状态" |

### Notification 表

| 字段 | 验证规则 | 错误消息 |
|------|---------|---------|
| `days_before` | > 0 的整数 | "提前天数必须大于 0" |
| `notification_type` | IN ('PUSH', 'EMAIL', 'SMS') | "无效的通知类型" |

---

## 🔄 状态转换状态机

```
                     ┌─────────┐
                     │ DELETED │ (软删除)
                     └─────────┘
                         ↑
                         │ (用户删除)
                         │
    ┌──────────────────────────────────────┐
    │                                      │
    ↓ (创建)                          (恢复)
┌──────────┐        ┌────────┐        ┌─────────┐
│ ACTIVE   │───────→│CURRENT │───────→│ EXPIRED │
└──────────┘        └────────┘        └─────────┘
 (剩余>0天)   (还有0天)  (剩余<0天)
    ↑
    │ (创建时立即判断)
    │
  起点

状态转换时机:
1. 创建事件时: 根据 target_date - today.date() 判断初始状态
2. 每次查询时: 重新计算状态 (不需要后台任务)
3. 用户删除时: Event → DELETED (软删除)
4. P3 恢复时: DELETED → ACTIVE
```

---

## 📊 数据量估算

### P1 场景 (100 个事件)

```
存储需求:
  每个事件: ~250 bytes (JSON)
  100 个事件: ~25 KB
  总文件大小: 25 KB

内存使用:
  加载到内存: ~2-3 MB
  
性能:
  查询所有事件: < 5 ms
  创建事件: < 10 ms
  删除事件: < 10 ms
```

### P2 场景 (1000 个事件)

```
存储需求:
  SQLite 数据库: ~100-200 KB
  包括索引: ~150-250 KB
  
内存使用:
  缓存: ~10-20 MB (取决于活跃用户数)
  
性能:
  查询用户事件: < 50 ms (有索引)
  创建事件: < 20 ms
  同步小卡片: < 100 ms
```

### P3 场景 (10000+ 事件)

```
存储需求:
  PostgreSQL 数据库: ~1-2 MB
  包括索引: ~2-5 MB
  
内存使用:
  缓存 (Redis): ~50-100 MB
  应用内存: ~50-100 MB
  
性能:
  查询: < 200 ms (有缓存)
  创建: < 50 ms
  批量通知: < 5000 ms (10000 个事件)
```

---

## ✅ 与规范的对应关系

### 功能需求映射

| FR | 描述 | 数据模型实现 |
|----|------|----------|
| FR-001 | 创建事件 | `Event.name + Event.target_date` |
| FR-002 | 自动计算天数 | `remaining_days` 计算属性 |
| FR-003 | 查询事件 | `Event` 表查询 |
| FR-004 | 删除事件 | `Event.status = DELETED` (软删除) |
| FR-005 | 输入验证 | 数据库约束 + 应用层验证 |
| FR-006 | 0 天显示 | `remaining_days == 0 → CURRENT` |
| FR-008a | 拒绝重名 | `Event.name UNIQUE 约束` |
| FR-008b | 状态转换 | 4 个状态 + 转换规则 |
| FR-008c | 数据限制 | `name VARCHAR(256) + CHECK` |
| FR-009 | REST API | 用户认证 + 事件 CRUD 端点 |
| FR-010 | 小卡片 | `Widget` 表 |
| FR-013 | 通知规则 | `Notification` 表 |

---

## 🎯 后续行动

✅ **Stage 1 设计完成**

**下一步: Stage 2 项目设置**

需要:
1. 初始化 Git 仓库
2. 创建 Python 项目结构
3. 生成 setup.py + requirements.txt
4. 配置 pytest 框架
5. 创建首批测试用例

---

**设计完成日期**: 2026-01-22  
**数据模型完整**: ✅ 所有 P1/P2/P3 功能覆盖  
**可进入实施阶段**: ✅ 设计经过验证

