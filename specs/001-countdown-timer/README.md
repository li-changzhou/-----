# 倒计时工具 - 快速参考

## 📋 项目概览

- **功能**: CLI 倒计时工具
- **分支**: `001-countdown-timer`
- **MVP 版本**: 1.0.0
- **状态**: 规范和计划完成，待实施

## 📚 核心文件

| 文件 | 用途 |
|---|---|
| [spec.md](spec.md) | 功能规范（用户故事、需求、验收场景） |
| [plan.md](plan.md) | 实施计划（技术设计、架构、阶段划分） |
| [tasks.md](tasks.md) | 任务列表（具体开发任务、依赖关系） |

## 🎯 用户故事优先级

| 优先级 | 故事 | MVP 包含 | 版本 |
|---|---|---|---|
| P1 | 基础倒计时 + CLI 界面 | ✅ | 1.0.0 |
| P2 | 暂停/恢复 | ❌ | 1.1.0 |
| P3 | 时间标记 | ❌ | 1.2.0 |

## 🏗️ 项目结构

```
countdown-timer/
├── src/                    # 源代码
│   ├── cli.py             # CLI 入口
│   ├── countdown.py       # 倒计时核心逻辑
│   ├── formatter.py       # 时间格式化
│   ├── notifier.py        # 完成通知
│   ├── config.py          # 配置管理
│   └── utils.py           # 工具函数
├── tests/                 # 测试
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   └── contract/          # 合约测试
└── docs/                  # 文档
```

## 🔄 开发流程（章程驱动）

1. **规范**: ✅ 已完成（spec.md）
2. **计划**: ✅ 已完成（plan.md）
3. **任务分解**: ✅ 已完成（tasks.md）
4. **实施**: ⏳ 下一步
   - 测试优先（TDD）：先编写测试，测试失败 → 实施代码 → 测试通过
   - 三层验证：单元测试、集成测试、合约测试
   - 目标覆盖率：≥ 95%

## 📝 核心功能（P1）

```bash
# 基本用法
countdown 5              # 5 分钟倒计时
countdown 2:30          # 2 分 30 秒倒计时
countdown --help        # 显示帮助

# 示例输出
$ countdown 2:30
Starting 2:30 countdown...
2:30
2:29
...
0:01
0:00
✅ Time's up!
```

## 🧪 测试策略

| 层级 | 文件模式 | 覆盖范围 |
|---|---|---|
| **单元** | `tests/unit/test_*.py` | 个别函数/类逻辑 |
| **集成** | `tests/integration/test_*.py` | CLI + 组件交互 |
| **合约** | `tests/contract/test_*.py` | CLI 接口定义 |

## 🚀 启动步骤

### 阶段 0: 准备（T001-T004）
```bash
cd countdown-timer
python -m venv venv
source venv/bin/activate  # 或 Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 阶段 1: 框架设置（T005-T010）
- 创建项目结构
- 配置 pytest
- 初始化数据模型

### 阶段 2: MVP 实施（T011-T026）
- 编写测试（T011-T015）→ 失败 ❌
- 实施代码（T016-T026）→ 测试通过 ✅
- 目标：P1 故事完全交付

## 📊 任务统计

| 阶段 | 任务数 | 重点 |
|---|---|---|
| 阶段 0 | 4 | 研究与准备 |
| 阶段 1 | 6 | 框架与工具链 |
| 阶段 2 | 16 | **MVP 实施** |
| 阶段 3 | 5 | P2 功能（可选） |
| 阶段 4 | 6 | P3 功能（可选） |
| 阶段 5 | 6 | 优化与发布 |
| **总计** | **43** | |

## ✅ 合规性检查清单

根据项目章程，本项目遵守：

- ✅ **规范驱动设计** - 规范包含完整用户故事和验收场景
- ✅ **测试优先** - 所有阶段都遵循 TDD
- ✅ **分层验证** - 合约、集成、单元、功能测试都有
- ✅ **可观测性** - 人类可读输出 + 结构化日志
- ✅ **版本管理** - 语义版本化（1.0.0 → 1.1.0 → 1.2.0）
- ✅ **简洁性** - MVP 仅包含必要功能
- ✅ **独立故事** - 每个故事能独立交付价值

## 🔗 相关文件

- 项目章程: [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md)
- 规范模板: [`.specify/templates/spec-template.md`](../../.specify/templates/spec-template.md)
- 计划模板: [`.specify/templates/plan-template.md`](../../.specify/templates/plan-template.md)
- 任务模板: [`.specify/templates/tasks-template.md`](../../.specify/templates/tasks-template.md)

---

**下一步**: 批准此规范，然后开始阶段 0 研究和阶段 1 框架设置。
