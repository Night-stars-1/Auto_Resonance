import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
print(project_root)
sys.path.append(str(project_root))

import pytest
from core.goods.srap import get_goods_info

class TestOneFLOW:
    def test_01(self):
        print("国产CFD开源软件OneFLOW自动测试-01")

    def test_02(self):
        print("国产CFD开源软件OneFLOW自动测试-02")

    def test_03(self):
        print("国产CFD开源软件OneFLOW自动测试-03")
        assert 1 == 3
