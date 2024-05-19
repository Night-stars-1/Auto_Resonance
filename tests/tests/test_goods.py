"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:45:55
LastEditTime: 2024-05-05 20:37:30
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

from core.models.goods import GoodsModel

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import logging

LOGGER = logging.getLogger(__name__)
from app.common.config import cfg
from core.api.kmou import get_goods_info as get_goods_info_kmou
from core.api.srap import get_goods_info as get_goods_info_srap
from core.goods import SHOP, show


def test_get_goods_info_srap():
    route = get_goods_info_srap()
    LOGGER.info(route)
    print(show(route))
    assert route.city_data[0].profit != 0 and route.city_data[1].profit != 0


def test_get_goods_info_kmou():
    route = get_goods_info_kmou()
    LOGGER.info(route)
    print(show(route))
    assert route.city_data[0].profit != 0 and route.city_data[1].profit != 0


def test_get_city_data_by_city_level():
    result = SHOP(goods_data=GoodsModel(goods=[])).get_city_data_by_city_level()
    print(result)
    assert result["7号自由港"].buy_num != 0.0


if __name__ == "__main__":
    # test_get_goods_info_kmou()
    test_get_goods_info_srap()
    # test_get_city_data_by_city_level()
