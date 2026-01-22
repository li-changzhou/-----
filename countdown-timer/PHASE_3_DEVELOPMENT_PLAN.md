# 🚀 Phase 3 开发计划 - Web UI + FastAPI

**阶段**: P3 (高级功能)  
**焦点**: Web UI 构建 + FastAPI 后端  
**预计时间**: 4-6 小时  
**状态**: 🔄 进行中  
**版本**: 0.2.0 (Web Edition)

---

## 📋 项目概览

```
Event Countdown Tool
    ↓
MVP (v0.1.0) ✅ 完成
    ↓
P3: Web UI + API (v0.2.0) 🔄 进行中
    ├── FastAPI 后端
    ├── REST API 端点
    ├── Web UI 前端
    └── 集成测试
```

---

## 🎯 Phase 3 目标

### 1. 后端升级 (FastAPI)
- [x] 设计 REST API 架构
- [ ] 安装 FastAPI 和 uvicorn
- [ ] 创建 API 路由（CRUD）
- [ ] 实现错误处理
- [ ] 添加 API 文档

### 2. 前端构建 (Web UI)
- [ ] 创建 HTML 模板
- [ ] 设计 CSS 样式
- [ ] 实现 JavaScript 交互
- [ ] 响应式设计
- [ ] 用户友好界面

### 3. 集成与测试
- [ ] 前后端集成
- [ ] 端到端测试
- [ ] 性能基准
- [ ] 用户验收测试

### 4. 部署准备
- [ ] Docker 容器化
- [ ] 环境配置
- [ ] 部署文档
- [ ] 快速启动脚本

---

## 📁 P3 项目结构

```
countdown-timer/
├── src/countdown_timer/
│   ├── api/                    # ✨ 新增
│   │   ├── __init__.py
│   │   ├── app.py             # FastAPI 应用
│   │   ├── routes.py          # API 路由
│   │   ├── schemas.py         # 数据验证
│   │   └── models.py          # Pydantic 模型
│   │
│   ├── web/                    # ✨ 新增
│   │   ├── __init__.py
│   │   ├── static/            # CSS、JS、图片
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── js/
│   │   │   │   └── app.js
│   │   │   └── images/
│   │   └── templates/         # HTML 模板
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── add-event.html
│   │       └── event-detail.html
│   │
│   ├── cli.py                 # 现有
│   ├── event_manager.py       # 现有
│   └── ...其他模块
│
├── tests/
│   ├── unit/                  # 现有
│   └── integration/           # ✨ 新增
│       ├── test_api.py
│       └── test_web.py
│
├── docker/                     # ✨ 新增
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt           # 更新
├── setup.py                   # 更新
├── app.py                     # ✨ 新增 (启动文件)
└── README_v0.2.md            # ✨ 新增
```

---

## 🔧 技术栈

### 后端
- **FastAPI** - 现代 Web 框架
- **Uvicorn** - ASGI 服务器
- **Pydantic** - 数据验证
- **Python 3.11+**

### 前端
- **HTML5** - 标记语言
- **CSS3** - 样式设计
- **Vanilla JavaScript** - 交互逻辑
- **Fetch API** - HTTP 通信

### 测试与部署
- **Pytest** - 现有测试框架
- **Docker** - 容器化
- **Docker Compose** - 编排

---

## 📊 REST API 设计

### 基础 URL
```
http://localhost:8000/api
```

### 端点设计

#### 事件操作

| 方法 | 端点 | 说明 | 状态码 |
|------|------|------|--------|
| GET | `/events` | 获取所有事件 | 200 |
| POST | `/events` | 创建新事件 | 201 |
| GET | `/events/{name}` | 获取事件详情 | 200 |
| PUT | `/events/{name}` | 更新事件 | 200 |
| DELETE | `/events/{name}` | 删除事件 | 204 |

#### 统计数据

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/stats` | 获取统计信息 |
| GET | `/stats/summary` | 获取摘要 |

#### 健康检查

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/health` | 服务健康状态 |

---

## 🎨 Web UI 设计

### 页面结构

```
首页 (Dashboard)
├── 事件列表
│   ├── 创建按钮
│   ├── 搜索框
│   └── 事件卡片网格
│       ├── 事件名称
│       ├── 倒计时
│       ├── 状态指示
│       ├── 编辑按钮
│       └── 删除按钮
│
├── 添加事件对话框
│   ├── 事件名称输入
│   ├── 日期选择器
│   └── 保存/取消按钮
│
└── 统计面板
    ├── 总事件数
    ├── 进行中事件
    ├── 已过期事件
    └── 下一个事件
```

### UI 特性

- 🎯 实时倒计时更新
- 🎨 现代化设计
- 📱 响应式布局
- ✨ 平滑动画
- ⌨️ 键盘快捷键
- 🌙 深色模式支持

---

## 📈 开发阶段

### 第 1 阶段：后端基础 (1-1.5 小时)
- [ ] 安装依赖
- [ ] 创建 FastAPI 应用
- [ ] 实现基本路由
- [ ] 测试 API 端点

### 第 2 阶段：前端框架 (1.5-2 小时)
- [ ] 创建 HTML 模板
- [ ] 编写 CSS 样式
- [ ] 实现 JavaScript 逻辑
- [ ] 集成 Fetch API

### 第 3 阶段：集成与优化 (1 小时)
- [ ] 前后端联调
- [ ] 功能测试
- [ ] 性能优化
- [ ] 问题修复

### 第 4 阶段：测试与部署 (1-1.5 小时)
- [ ] 编写集成测试
- [ ] Docker 配置
- [ ] 部署验证
- [ ] 文档编写

---

## 🚀 快速启动预览

```bash
# Phase 3 完成后的启动方式
cd countdown-timer

# 方式 1: CLI (v0.1.0)
countdown add "生日" "2026-03-15"
countdown list

# 方式 2: FastAPI Web (v0.2.0) - 新增
python app.py
# 访问: http://localhost:8000

# 或使用 Docker
docker-compose up
# 访问: http://localhost:8000
```

---

## 📝 检查清单

### 后端检查
- [ ] FastAPI 应用创建
- [ ] 所有 CRUD 路由实现
- [ ] 数据验证完成
- [ ] 错误处理完善
- [ ] API 文档生成
- [ ] 单元测试通过
- [ ] 集成测试通过

### 前端检查
- [ ] HTML 模板创建
- [ ] CSS 样式完成
- [ ] JavaScript 功能实现
- [ ] 响应式设计验证
- [ ] 跨浏览器测试
- [ ] 性能优化
- [ ] 无网络请求错误

### 集成检查
- [ ] 前后端通信成功
- [ ] 实时更新工作
- [ ] 错误处理正确
- [ ] 性能达标
- [ ] 用户体验良好

### 部署检查
- [ ] Docker 构建成功
- [ ] 容器运行正常
- [ ] 所有端口开放
- [ ] 文档完整

---

## 💡 技术亮点

### 后端创新
- 现代 FastAPI 框架
- 自动 API 文档 (Swagger)
- 类型提示和验证
- 异步支持

### 前端创新
- 响应式设计
- 实时数据更新
- 平滑用户体验
- 离线支持 (计划)

### 集成创新
- 一个代码库
- CLI + Web 双模式
- Docker 容器化
- 易于部署

---

## 📚 相关文档

- [FINAL_PROJECT_REPORT.md](FINAL_PROJECT_REPORT.md) - P1 完成报告
- [STAGE3_COMPLETION_SUMMARY.md](STAGE3_COMPLETION_SUMMARY.md) - 阶段总结
- [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) - 导航指南

---

## 🎯 Success Criteria

| 标准 | 指标 | 目标 |
|------|------|------|
| 功能完整 | 5 个 API 端点 | ✅ 全部实现 |
| 前端体验 | 4 个主要页面 | ✅ 全部完成 |
| 代码质量 | 集成测试覆盖 | ✅ 80% 以上 |
| 性能 | API 响应时间 | <200ms |
| 部署 | Docker 支持 | ✅ 完成 |

---

**开始时间**: 2026-01-22  
**版本**: 0.2.0 (Web Edition)  
**状态**: 🔄 Phase 3 进行中
