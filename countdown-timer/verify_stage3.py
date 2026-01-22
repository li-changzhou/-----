"""
Stage 3 功能验证脚本

验证所有 8 个接受场景的完整工作流
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime, date, timedelta

# 配置
PYTHON_EXE = "D:/ZM/dragontrail/ai/test/.venv/Scripts/python.exe"
CLI_CMD = [PYTHON_EXE, "-m", "src.countdown_timer.cli"]
STORAGE_DIR = Path.home() / ".countdown"

# 颜色输出
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def run_command(cmd):
    """运行 CLI 命令"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def print_result(scenario, passed, message=""):
    """打印测试结果"""
    status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    print(f"{status} | {scenario}")
    if message:
        print(f"  └─ {message}")

def verify_storage_exists():
    """验证存储文件存在"""
    return (STORAGE_DIR / "events.json").exists()

def get_stored_events():
    """读取存储的事件"""
    if not verify_storage_exists():
        return {}
    with open(STORAGE_DIR / "events.json") as f:
        return json.load(f)

# =============== 场景测试 ===============

def scenario_1_create_event():
    """S1: 创建事件 (FR-001)"""
    print(f"\n{BLUE}[S1] 创建事件{RESET}")
    
    code, out, err = run_command(CLI_CMD + ["add", "生日", "2026-03-15"])
    passed = code == 0 and "生日" in out
    print_result("S1: 创建事件", passed, out.strip() if passed else err.strip())
    
    # 验证数据持久化
    events = get_stored_events()
    has_event = "生日" in events
    print_result("S1: 数据持久化", has_event, f"事件已保存: {has_event}")
    
    return passed and has_event

def scenario_2_same_day_countdown():
    """S2: 同日倒计时 (FR-006)"""
    print(f"\n{BLUE}[S2] 同日倒计时{RESET}")
    
    today = date.today().isoformat()
    code, out, err = run_command(CLI_CMD + ["add", "今天", today])
    passed = code == 0
    print_result("S2: 创建今日事件", passed, out.strip() if passed else err.strip())
    
    # 验证显示 0 天
    code, out, err = run_command(CLI_CMD + ["show", "今天"])
    has_zero_days = "0 天" in out or "0天" in out
    print_result("S2: 显示 0 天", has_zero_days, out.strip() if has_zero_days else "未显示 0 天")
    
    return passed and has_zero_days

def scenario_3_list_all_events():
    """S3: 列出所有事件 (FR-003)"""
    print(f"\n{BLUE}[S3] 列出所有事件{RESET}")
    
    code, out, err = run_command(CLI_CMD + ["list"])
    passed = code == 0
    print_result("S3: 列出命令", passed, f"找到 {out.count('.')} 个事件")
    
    # 验证显示多个事件
    has_events = "生日" in out and "今天" in out
    print_result("S3: 显示多个事件", has_events, "生日和今天都已显示")
    
    return passed and has_events

def scenario_4_delete_event():
    """S4: 删除事件 (FR-004)"""
    print(f"\n{BLUE}[S4] 删除事件{RESET}")
    
    code, out, err = run_command(CLI_CMD + ["delete", "今天"])
    passed = code == 0
    print_result("S4: 删除命令", passed, out.strip() if passed else err.strip())
    
    # 验证事件已删除
    code, out, err = run_command(CLI_CMD + ["list"])
    not_exists = "今天" not in out
    print_result("S4: 事件已删除", not_exists, "列表中不再显示")
    
    return passed and not_exists

def scenario_5_reject_invalid_date():
    """S5: 拒绝无效日期 (FR-005)"""
    print(f"\n{BLUE}[S5] 拒绝无效日期{RESET}")
    
    # 测试各种无效格式
    invalid_dates = [
        ("2026/03/15", "斜杠格式"),
        ("15-03-2026", "反向格式"),
        ("2026-13-01", "无效月份"),
        ("abc", "非日期"),
    ]
    
    all_rejected = True
    for invalid_date, desc in invalid_dates:
        code, out, err = run_command(CLI_CMD + ["add", f"测试_{desc}", invalid_date])
        rejected = code != 0
        print_result(f"S5: 拒绝 {desc}", rejected)
        all_rejected = all_rejected and rejected
    
    return all_rejected

def scenario_6_show_expired_event():
    """S6: 显示已过期事件 (FR-008b)"""
    print(f"\n{BLUE}[S6] 显示已过期事件{RESET}")
    
    # 创建过期事件
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    code, out, err = run_command(CLI_CMD + ["add", "过期事件", yesterday])
    created = code == 0
    print_result("S6: 创建过期事件", created)
    
    # 验证状态
    code, out, err = run_command(CLI_CMD + ["show", "过期事件"])
    is_expired = "已过期" in out or "EXPIRED" in out
    print_result("S6: 显示过期状态", is_expired, out.strip() if is_expired else "未标记为过期")
    
    return created and is_expired

def scenario_7_reject_duplicate():
    """S7: 拒绝重复名称 (FR-008a)"""
    print(f"\n{BLUE}[S7] 拒绝重复名称{RESET}")
    
    # 创建第一个事件
    code1, out1, err1 = run_command(CLI_CMD + ["add", "重复测试", "2026-05-01"])
    created = code1 == 0
    print_result("S7: 创建事件", created)
    
    # 尝试创建重复事件
    code2, out2, err2 = run_command(CLI_CMD + ["add", "重复测试", "2026-06-01"])
    rejected = code2 != 0
    print_result("S7: 拒绝重复", rejected, "无法创建重复事件")
    
    return created and rejected

def scenario_8_boundary_recalculation():
    """S8: 边界重新计算 (FR-006)"""
    print(f"\n{BLUE}[S8] 边界重新计算{RESET}")
    
    # 创建明天的事件
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    code, out, err = run_command(CLI_CMD + ["add", "明天", tomorrow])
    created = code == 0
    print_result("S8: 创建明日事件", created)
    
    # 验证显示 1 天
    code, out, err = run_command(CLI_CMD + ["show", "明天"])
    has_one_day = "1 天" in out or "1天" in out
    print_result("S8: 显示 1 天", has_one_day, out.strip() if has_one_day else "未正确显示天数")
    
    # 验证边界数据
    events = get_stored_events()
    has_boundary = "明天" in events
    print_result("S8: 边界数据存储", has_boundary)
    
    return created and has_one_day and has_boundary

# =============== 主函数 ===============

def main():
    """执行所有场景测试"""
    print(f"{BLUE}{'='*60}")
    print(f"Stage 3 - 功能完整验证")
    print(f"{'='*60}{RESET}\n")
    
    # 清理旧数据
    print(f"{YELLOW}准备: 清理旧数据...{RESET}")
    if STORAGE_DIR.exists():
        import shutil
        shutil.rmtree(STORAGE_DIR)
    
    # 创建存储目录
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{GREEN}✓ 存储目录已初始化{RESET}\n")
    
    # 运行场景测试
    results = {
        "S1: 创建事件": scenario_1_create_event(),
        "S2: 同日倒计时": scenario_2_same_day_countdown(),
        "S3: 列出所有": scenario_3_list_all_events(),
        "S4: 删除事件": scenario_4_delete_event(),
        "S5: 拒绝无效": scenario_5_reject_invalid_date(),
        "S6: 显示已过期": scenario_6_show_expired_event(),
        "S7: 拒绝重复": scenario_7_reject_duplicate(),
        "S8: 边界重算": scenario_8_boundary_recalculation(),
    }
    
    # 生成报告
    print(f"\n{BLUE}{'='*60}")
    print(f"测试总结")
    print(f"{'='*60}{RESET}\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for scenario, result in results.items():
        status = f"{GREEN}✅{RESET}" if result else f"{RED}❌{RESET}"
        print(f"{status} {scenario}")
    
    print(f"\n{BLUE}总体: {passed}/{total} 场景通过{RESET}")
    
    if passed == total:
        print(f"{GREEN}{'='*60}")
        print(f"🎉 所有场景验证通过！")
        print(f"{'='*60}{RESET}")
        return 0
    else:
        print(f"{RED}{'='*60}")
        print(f"⚠️  {total - passed} 个场景失败")
        print(f"{'='*60}{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
