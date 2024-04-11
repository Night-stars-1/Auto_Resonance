"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:45:55
LastEditTime: 2024-04-11 19:47:34
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import logging

LOGGER = logging.getLogger(__name__)
from core.goods.srap import get_goods_info


def test_get_goods_info():
    route = get_goods_info()
    LOGGER.info(route)
    assert route[0].profit != 0 and route[1].profit != 0
