"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:45:55
LastEditTime: 2024-04-12 20:38:00
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import logging

LOGGER = logging.getLogger(__name__)
from core.goods.shop import show
from core.goods.srap import get_goods_info


def test_get_goods_info():
    route = get_goods_info(
        {
            "7号自由港": 3,
            "修格里城": 3,
            "曼德矿场": 3,
            "淘金乐园": 3,
            "澄明数据中心": 3,
            "荒原站": 3,
            "铁盟哨站": 3,
            "阿妮塔战备工厂": 3,
            "阿妮塔能源研究所": 3,
            "priceThreshold": 500,
        }
    )
    LOGGER.info(route)
    print(show(route))
    assert route.city_data[0].profit != 0 and route.city_data[1].profit != 0


if __name__ == "__main__":
    test_get_goods_info()
