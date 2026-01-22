---
description: "倒计时工具实现任务列表"
---

# 任务: 倒计时工具

**输入**: 来自 `/specs/001-countdown-timer/` 的设计文档
**前置条件**: plan.md(必需)、spec.md(用户故事必需)、research.md、data-model.md

⚠️ **强制要求**（章程驱动）: 此任务列表遵循**测试优先**原则。每个用户故事的测试必须**在实施前编写并失败**，然后实施代码使其通过。测试不可选。

**组织结构**: 任务按用户故事分组，以便每个故事能够独立实施和测试。

## 格式: `[ID] [P] [Story] 描述`
- **[P]**: 可以并行运行(不同文件, 无依赖关系)
- **[Story]**: 此任务属于哪个用户故事(例如: US1、US2、US3)
- 在描述中包含确切的文件路径

## 路径约定
- **项目根目录**: `countdown-timer/`
- **源代码**: `countdown-timer/src/`
- **测试**: `countdown-timer/tests/`

---

## 阶段 0: 研究与准备

**目的**: 环境和依赖验证

- [ ] T001 研究 Python 3.11 跨平台时间精度（Linux/macOS/Windows）
- [ ] T002 评估 Click 4.1 vs argparse，记录优缺点至 `research.md`
- [ ] T003 验证 playsound 跨平台兼容性和替代方案
- [ ] T004 创建虚拟环境并安装依赖：pytest、Click、playsound

---

## 阶段 1: 设置与框架 (共享基础设施)

**目的**: 项目结构初始化和测试框架就绪

**⚠️ 关键**: 在此阶段完成之前，无法开始任何用户故事工作

- [ ] T005 创建项目目录结构（src/、tests/、docs/）
- [ ] T006 初始化 Python 项目：setup.py、requirements.txt、pytest.ini
- [ ] T007 [P] 创建 `src/__init__.py` 和基础模块框架
- [ ] T008 [P] 配置 pytest 并设置测试覆盖（target: 95%+）
- [ ] T009 [P] 设置 .gitignore 和 CI/CD 工作流框架
- [ ] T010 创建 `data-model.md`，定义 Countdown、TimeMark、Config 实体

**检查点**: 项目框架就绪 - 现在可以开始编写测试和实施

---

## 阶段 2: 用户故事 1 - CLI 倒计时器基础功能 (P1) 🎯 MVP

**目标**: 实现可用的 CLI 倒计时工具，支持基本计时、进度显示、完成通知

**独立测试**: 通过 CLI 命令运行倒计时、验证每秒递减、确认完成通知；此故事完成后可作为独立应用交付给用户

### 用户故事 1 的测试（测试优先 - 必须先编写这些测试，确保在实施前失败）

- [ ] T011 [P] [US1] 在 `tests/contract/test_cli_contract.py` 中编写 CLI 接口合约测试
  - 测试 `countdown --help` 输出使用信息
  - 测试 `countdown 5` 接受有效的分钟参数
  - 测试 `countdown 2:30` 接受 MM:SS 格式
  - 测试 `countdown invalid` 拒绝无效参数

- [ ] T012 [P] [US1] 在 `tests/unit/test_countdown.py` 中编写倒计时逻辑单元测试
  - 测试 Countdown 类初始化：设定时间、状态、精度
  - 测试 `tick()` 方法：每次调用递减 1 秒
  - 测试 `is_complete()` 方法：时间到达 0 时返回 True
  - 测试 `get_remaining()` 方法：返回正确的剩余时间
  - 测试 `pause()` 和 `resume()` 方法的状态转换

- [ ] T013 [P] [US1] 在 `tests/unit/test_formatter.py` 中编写格式化单元测试
  - 测试 `format_time(300)` 返回 "5:00"
  - 测试 `format_time(150)` 返回 "2:30"
  - 测试 `format_time(3661)` 返回 "1:01:01"（超过 1 小时）
  - 测试 `format_time(0)` 返回 "0:00"

- [ ] T014 [P] [US1] 在 `tests/unit/test_notifier.py` 中编写通知单元测试
  - 测试 `notify_completion()` 方法调用
  - 测试输出包含完成消息

- [ ] T015 [P] [US1] 在 `tests/integration/test_cli_basic.py` 中编写集成测试
  - 集成测试：运行 CLI 倒计时 3 秒，验证输出进度
  - 集成测试：验证 Ctrl+C 优雅中止
  - 集成测试：验证完成后输出完成消息

### 用户故事 1 的实施

- [ ] T016 [P] [US1] 在 `src/countdown.py` 中创建 `Countdown` 类
  - 属性：total_seconds、remaining_seconds、status（运行中/暂停/完成）
  - 方法：`tick()`、`is_complete()`、`get_remaining()`、`get_elapsed()`
  - 确保所有单元测试通过

- [ ] T017 [P] [US1] 在 `src/formatter.py` 中创建 `Formatter` 类
  - 方法：`format_time(seconds)` 返回 "M:SS" 或 "H:MM:SS" 格式
  - 支持人类可读输出和 JSON 格式
  - 确保所有单元测试通过

- [ ] T018 [P] [US1] 在 `src/notifier.py` 中创建 `Notifier` 类
  - 方法：`notify_completion(remaining_time)` 输出完成消息
  - 尽力播放系统蜂鸣器或提示音
  - 测试通过时无需真实声音，使用 mock

- [ ] T019 [US1] 在 `src/cli.py` 中实施 CLI 入口点（依赖于 T016、T017、T018）
  - 使用 Click 框架定义 `countdown` 命令
  - 参数：时间（分钟或 MM:SS 格式）
  - 解析输入时间、创建 Countdown 实例
  - 主循环：每秒调用 `tick()`、刷新显示、检查完成
  - 处理 Ctrl+C 中止

- [ ] T020 [US1] 在 `src/utils.py` 中创建辅助函数
  - `parse_time_input(input_str)` 解析 "5" 或 "2:30" 格式
  - 验证输入有效性（正数、有效格式）
  - 所有相关单元测试通过

- [ ] T021 [US1] 在 `src/config.py` 中创建 `CountdownConfig` 类
  - 配置：启用声音、输出格式、日志级别
  - 从环境变量或命令行参数加载

- [ ] T022 [US1] 实施集成测试验证 E2E 流程
  - 运行集成测试确保 CLI + 计时器 + 格式化 + 通知协同工作
  - 所有集成测试通过

- [ ] T023 [US1] 实施合约测试验证 CLI 接口
  - CLI 接受有效输入、拒绝无效输入
  - 输出格式符合规范
  - 所有合约测试通过

- [ ] T024 [US1] 添加错误处理和日志
  - 无效输入的友好错误消息
  - 结构化日志（可选 JSON 模式）
  - 调试信息：启动时间、精度验证

- [ ] T025 [US1] 在 `docs/README.md` 中创建项目文档
  - 功能概述、安装说明、使用示例
  - 参数和选项说明

- [ ] T026 [US1] 在 `docs/USAGE.md` 中创建使用指南
  - 常见使用场景示例
  - 命令参考

**检查点**: P1 故事完成 - 倒计时工具现在可用。所有单元/集成/合约测试通过，代码覆盖 ≥95%，文档完整。此时可将 v1.0.0 作为 MVP 交付。

---

## 阶段 3: 用户故事 2 - 暂停和恢复功能 (P2)

**目标**: 添加暂停/恢复能力，丰富用户体验

**前置条件**: P1 故事完全完成

- [ ] T027 [P] [US2] 在 `tests/unit/test_countdown.py` 中添加暂停/恢复单元测试
  - 测试 `pause()` 方法：状态变为"暂停"，时间停止递减
  - 测试 `resume()` 方法：状态变为"运行中"，时间继续递减
  - 测试不可在已完成状态下暂停/恢复

- [ ] T028 [US2] 在 `src/countdown.py` 中实施暂停/恢复逻辑（依赖于 T027）
  - 添加 `pause()` 和 `resume()` 方法
  - 管理状态转换
  - 单元测试通过

- [ ] T029 [P] [US2] 在 `tests/integration/test_cli_pause_resume.py` 中编写集成测试
  - 运行倒计时、按空格暂停、验证停止
  - 再次按空格恢复、验证继续
  - 按 'r' 显示剩余时间

- [ ] T030 [US2] 在 `src/cli.py` 中添加暂停/恢复命令绑定（依赖于 T028、T029）
  - 空格键绑定暂停/恢复
  - 'r' 键显示剩余时间
  - 集成测试通过

- [ ] T031 [US2] 更新 `docs/USAGE.md`，添加暂停/恢复用法

**检查点**: P2 功能完成 - 倒计时工具现在支持暂停/恢复。所有测试通过，版本升级至 1.1.0。

---

## 阶段 4: 用户故事 3 - 时间标记功能 (P3)

**目标**: 添加分段时间追踪能力

**前置条件**: P2 故事完全完成

- [ ] T032 [P] [US3] 在 `tests/unit/test_timemark.py` 中编写 TimeMark 单元测试
  - 测试 `TimeMark` 类初始化和属性
  - 测试时间标记记录和排序

- [ ] T033 [US3] 在 `src/countdown.py` 中添加时间标记管理（依赖于 T032）
  - 添加 `mark()` 方法记录时间检查点
  - 添加 `get_marks()` 方法返回所有标记
  - 单元测试通过

- [ ] T034 [P] [US3] 在 `tests/integration/test_cli_marks.py` 中编写集成测试
  - 运行倒计时、按 'm' 键标记时间
  - 完成后显示所有标记和时间段

- [ ] T035 [US3] 在 `src/cli.py` 中添加标记命令绑定（依赖于 T033、T034）
  - 'm' 键绑定时间标记
  - 完成时显示标记摘要
  - 集成测试通过

- [ ] T036 [US3] 在 `src/formatter.py` 中添加标记显示格式
  - `format_marks(marks)` 返回格式化的标记列表和时间段

- [ ] T037 [US3] 更新 `docs/USAGE.md`，添加时间标记用法

**检查点**: P3 功能完成 - 倒计时工具现在支持时间标记。所有测试通过，版本升级至 1.2.0。

---

## 阶段 5: 优化与发布

- [ ] T038 运行完整测试套件，确保覆盖率 ≥ 95%
- [ ] T039 代码审查和重构，去除重复代码
- [ ] T040 性能测试：精度验证、CPU 占用率检查
- [ ] T041 创建 setup.py 和发布脚本
- [ ] T042 创建 DEVELOPMENT.md，开发者指南
- [ ] T043 最终文档审查

**发布**: v1.0.0（仅 P1）、v1.1.0（+ P2）、v1.2.0（+ P3）

---

## 任务依赖图

```
Phase 1 (T005-T010: 框架)
         ↓
Phase 2 (T011-T026: 测试 → 实施)
         ↓
Phase 3 (T027-T031: P2 功能)
         ↓
Phase 4 (T032-T037: P3 功能)
         ↓
Phase 5 (T038-T043: 优化发布)
```

---

**注**: 所有测试必须先编写并确认失败，然后实施代码使其通过（TDD 模式）。
