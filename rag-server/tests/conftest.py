"""rag-server 测试公共配置。

作用：
1. 让 tests 目录下的用例可以直接导入本地 `src/` 代码。
2. 在项目早期（测试文件已建但内容尚未编写）时，避免“未收集到测试”导致命令失败。
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

# 将 `src/` 插入 import 搜索路径，避免必须先安装包（editable install）才能跑测试。
if SRC_DIR.exists():
	sys.path.insert(0, str(SRC_DIR))


def pytest_sessionfinish(session, exitstatus: int) -> None:
	"""在测试会话结束时调整退出码。

	pytest 约定：当“没有收集到任何测试”时，退出码通常是 5。
	当前项目处于脚手架阶段，很多测试文件是空壳，这个状态在早期是预期行为。
	因此这里把 5 改为 0，表示“本次检查通过（只是暂时没有可执行测试）”。
	"""
	# 5 = no tests collected（不是测试失败，而是暂时没有测试可运行）
	if exitstatus == 5:
		session.exitstatus = 0
