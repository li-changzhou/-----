# Stage 3: P1 MVP 实现与发布 - 项目计划

**阶段**: Stage 3  
**目标**: P1 (MVP) 完整实现、打包、发布  
**当前状态**: ✅ Stage 2 已完成，准备进入 Stage 3  
**开始日期**: 2026-01-22

---

## 阶段目标

将 Stage 2 的完整代码库转化为可用的产品级应用：

✅ **完整功能验证** - 所有场景端到端测试  
✅ **生产打包** - 创建可分发包  
✅ **部署准备** - 为实际使用准备  
✅ **用户文档** - 完整的使用指南  
✅ **质量保证** - 最终 QA 检查

---

## 当前基线 (Stage 2 完成)

```
代码质量:      95% 覆盖率 ✅
功能完整性:    10/10 需求 ✅
测试通过率:    65/65 测试 100% ✅
执行时间:      0.76 秒 ✅
```

---

## Stage 3 任务分解

### 任务 1: 功能完整验证 (当前优先级: 🔴 立即)

**目标**: 端到端验证所有 8 个接受场景

| 任务 | 场景 | 验证方式 | 状态 |
|------|------|---------|------|
| 1.1 | 创建事件 | 手动测试 + 集成测试 | ⏳ |
| 1.2 | 同日倒计时 | 日期边界测试 | ⏳ |
| 1.3 | 列出所有 | CLI 命令验证 | ⏳ |
| 1.4 | 删除事件 | 清理验证 | ⏳ |
| 1.5 | 拒绝无效 | 错误处理验证 | ⏳ |
| 1.6 | 显示已过期 | 状态转换验证 | ⏳ |
| 1.7 | 拒绝重复 | 重复检测验证 | ⏳ |
| 1.8 | 边界重算 | 时间流逝模拟 | ⏳ |

**预计时间**: 30 分钟

---

### 任务 2: CLI 入口点优化 (优先级: 🟡 高)

**目标**: 使 CLI 可直接执行，而不需要 `python -m`

**选项 A**: 创建可执行包入口点

```bash
# setup.py 配置
entry_points={
    'console_scripts': [
        'countdown=src.countdown_timer.cli:cli',
    ],
}
```

**选项 B**: 创建独立脚本

```bash
#!/usr/bin/env python
# countdown (可执行脚本)
from src.countdown_timer.cli import cli
if __name__ == '__main__':
    cli()
```

**预计时间**: 15 分钟  
**测试**: `countdown --help` 应该可直接执行

---

### 任务 3: 集成测试编写 (优先级: 🟡 高)

**目标**: 创建 `tests/integration/` 测试套件

**测试套件**: `test_workflow.py`

```python
# 完整工作流测试
class TestCompleteWorkflow:
    def test_user_creates_multiple_events(self):
        """用户创建多个事件的完整场景"""
    
    def test_event_lifecycle(self):
        """事件从创建到过期的完整生命周期"""
    
    def test_data_persistence(self):
        """跨会话数据持久化验证"""
```

**预计时间**: 45 分钟  
**目标覆盖率**: 追加 5-10% 覆盖

---

### 任务 4: 打包和发布 (优先级: 🟠 中)

**目标**: 创建可分发的包

**4.1 标准 Python 包**
```bash
python setup.py sdist bdist_wheel
# 输出: dist/countdown-timer-0.1.0.tar.gz 等
```

**4.2 可执行程序** (可选)
```bash
pip install pyinstaller
pyinstaller --onefile src/countdown_timer/cli.py
# 输出: dist/cli.exe
```

**4.3 Docker 镜像** (可选)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -e .
ENTRYPOINT ["countdown"]
```

**预计时间**: 30 分钟

---

### 任务 5: 用户文档 (优先级: 🟡 高)

**5.1 安装指南** (INSTALL.md)
- 系统要求
- 安装步骤
- 验证安装

**5.2 使用手册** (USAGE.md)
- 命令详解
- 常见场景
- 示例

**5.3 故障排除** (TROUBLESHOOTING.md)
- 常见问题
- 解决方案
- 联系方式

**5.4 变更日志** (CHANGELOG.md)
- v0.1.0 功能列表

**预计时间**: 45 分钟

---

### 任务 6: 最终 QA (优先级: 🟡 高)

**6.1 功能测试清单**
- [ ] 所有 4 个命令工作
- [ ] 错误消息清晰
- [ ] 帮助信息完整
- [ ] 没有崩溃

**6.2 性能测试**
- [ ] CLI 响应 < 100ms
- [ ] 支持 100+ 事件
- [ ] 内存使用 < 50MB

**6.3 兼容性测试**
- [ ] Windows 兼容 ✅
- [ ] macOS 兼容 ❓
- [ ] Linux 兼容 ❓

**6.4 安全测试**
- [ ] 无 SQL 注入
- [ ] 无路径遍历
- [ ] 文件权限正确

**预计时间**: 1 小时

---

## 详细执行计划

### 第 1 天 (今天): 立即行动

```
1. 功能完整验证 (30 分钟)
   ├─ 清理存储
   ├─ 逐个验证 8 个接受场景
   └─ 记录任何问题

2. CLI 入口点优化 (15 分钟)
   ├─ 更新 setup.py 添加 entry_points
   ├─ 重新安装 pip install -e .
   └─ 测试 countdown --help

3. 集成测试编写 (45 分钟)
   ├─ 创建 tests/integration/test_workflow.py
   ├─ 编写 3-4 个集成测试
   └─ 运行并验证
```

**第 1 天目标**: 完成任务 1-3

---

### 第 2 天: 打包和文档

```
4. 打包和发布 (30 分钟)
   ├─ python setup.py sdist bdist_wheel
   ├─ 验证包内容
   └─ 测试包安装

5. 用户文档 (45 分钟)
   ├─ 编写 INSTALL.md
   ├─ 编写 USAGE.md
   └─ 编写 TROUBLESHOOTING.md

6. 最终 QA (1 小时)
   ├─ 功能清单验证
   ├─ 性能基准测试
   └─ 安全审计
```

**第 2 天目标**: 完成任务 4-6，准备发布

---

## 详细任务说明

### 任务 1.1: 验证创建事件

**步骤**:
```bash
# 1. 清理旧数据
rm -rf ~/.countdown/

# 2. 创建事件
countdown add "生日" "2026-03-15"

# 3. 验证输出
# 预期: "✅ 生日 已创建，还有 52 天"
```

**验证检查**:
- ✅ 返回码为 0
- ✅ 消息包含事件名
- ✅ 显示剩余天数
- ✅ 事件已保存到文件

---

### 任务 1.2: 验证同日倒计时

**步骤**:
```bash
# 获取今天的日期 (当前: 2026-01-22)
countdown add "今天的事" "2026-01-22"

# 验证输出
# 预期: "✅ 今天的事 已创建，还有 0 天"
```

---

### 任务 2.1: 更新 setup.py

```python
# 添加到 setup() 调用
entry_points={
    'console_scripts': [
        'countdown=src.countdown_timer.cli:cli',
    ],
}
```

**验证**:
```bash
pip install -e .
which countdown  # 应该能找到
countdown --help  # 应该工作
```

---

### 任务 3.1: 创建集成测试

**文件**: `tests/integration/test_workflow.py`

```python
import pytest
from click.testing import CliRunner
from src.countdown_timer.cli import cli
import tempfile
import os

@pytest.fixture
def isolated_cli(monkeypatch):
    """隔离的 CLI 环境"""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setenv("COUNTDOWN_HOME", tmpdir)
        yield CliRunner()

class TestCompleteWorkflow:
    
    def test_user_creates_multiple_events(self, isolated_cli):
        """完整场景: 用户创建多个事件、列出、显示、删除"""
        runner = isolated_cli
        
        # 创建第一个事件
        result = runner.invoke(cli, ["add", "生日", "2026-03-15"])
        assert result.exit_code == 0
        
        # 创建第二个事件
        result = runner.invoke(cli, ["add", "假期", "2026-07-01"])
        assert result.exit_code == 0
        
        # 列出所有事件
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "生日" in result.output
        assert "假期" in result.output
        
        # 删除一个事件
        result = runner.invoke(cli, ["delete", "生日"])
        assert result.exit_code == 0
        
        # 验证删除
        result = runner.invoke(cli, ["list"])
        assert "假期" in result.output
        assert "生日" not in result.output
```

---

### 任务 5.1: 编写 INSTALL.md

```markdown
# 安装指南

## 系统要求

- Python 3.11 或更高版本
- pip (Python 包管理器)

## 安装步骤

### 方式 1: 从源代码安装 (开发)

\`\`\`bash
git clone <repo>
cd countdown-timer
pip install -e .
\`\`\`

### 方式 2: 从包安装 (发布版本)

\`\`\`bash
pip install countdown-timer==0.1.0
\`\`\`

## 验证安装

\`\`\`bash
countdown --help
\`\`\`

输出应该显示帮助信息。
```

---

## 检查清单

### 完成标准

- [ ] 所有 8 个接受场景端到端验证 ✅
- [ ] CLI 入口点可直接执行 ✅
- [ ] 集成测试编写完成 ✅
- [ ] 打包成功创建 ✅
- [ ] 用户文档完整 ✅
- [ ] 最终 QA 通过 ✅
- [ ] 版本号设置 (0.1.0) ✅
- [ ] 变更日志更新 ✅
- [ ] 没有遗留问题 ✅

### 交付物

- ✅ 可执行的 Python 包
- ✅ 完整的用户文档
- ✅ 集成测试套件
- ✅ 打包的分发包
- ✅ 最终 QA 报告

---

## 时间估算

| 任务 | 估计 | 实际 |
|------|------|------|
| 1. 功能验证 | 30 分钟 | ⏳ |
| 2. CLI 优化 | 15 分钟 | ⏳ |
| 3. 集成测试 | 45 分钟 | ⏳ |
| 4. 打包发布 | 30 分钟 | ⏳ |
| 5. 用户文档 | 45 分钟 | ⏳ |
| 6. 最终 QA | 60 分钟 | ⏳ |
| **总计** | **3.25 小时** | ⏳ |

---

## 风险评估

| 风险 | 可能性 | 影响 | 缓解 |
|------|--------|------|------|
| CLI 入口点冲突 | 低 | 中 | 用户名空间隔离 |
| 集成测试复杂 | 中 | 低 | 使用夹具简化 |
| 文档遗漏 | 低 | 中 | 检查清单验证 |
| 打包问题 | 低 | 中 | 测试安装验证 |

---

## 后续阶段

### P2 (扩展) - 可选
- SQLite 数据库集成
- REST API (FastAPI)
- 移动应用同步

### P3 (增强) - 可选
- 通知系统
- 事件共享
- 团队协作

---

## 参考文档

- [Stage 2 完成报告](STAGE2_COMPLETION_REPORT.md)
- [Stage 3 就绪检查](STAGE3_READINESS_CHECKLIST.md)
- [测试总结](TEST_SUMMARY.md)
- [项目交接总结](HANDOFF_SUMMARY.md)

---

## 开始步骤

**立即开始任务 1 (功能完整验证)**:

```bash
# 1. 进入项目目录
cd countdown-timer

# 2. 清理旧数据
rm -rf ~/.countdown/

# 3. 验证基本功能
python -m src.countdown_timer.cli add "测试" "2026-12-31"
python -m src.countdown_timer.cli list
python -m src.countdown_timer.cli show "测试"
python -m src.countdown_timer.cli delete "测试"

# 4. 所有测试应该通过
pytest tests/unit/ -v
```

---

**状态**: ✅ 准备就绪  
**下一步**: 开始 Stage 3 任务 1  
**预计完成**: 2026-01-23 下午

---

**Stage 3 项目计划 - 完成**
