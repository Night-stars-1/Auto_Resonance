"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:45:55
LastEditTime: 2024-04-14 16:36:15
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import logging

LOGGER = logging.getLogger(__name__)
from app.common.config import cfg
from core.api.kmou import get_goods_info as get_goods_info_kmou
from core.goods.shop import show
from core.api.srap import get_goods_info as get_goods_info_srap


def test_get_goods_info_srap():
    route = get_goods_info_srap(
        city_book={
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
        },
        skill_level={
            "伊尔": 0,
            "卡洛琳": 0,
            "叶珏": 0,
            "塞西尔": 0,
            "多萝西": 0,
            "奈弥": 0,
            "山岚": 0,
            "星花": 0,
            "朱利安": 2,
            "狮鬃": 0,
            "瑞秋": 0,
            "瓦伦汀": 0,
            "艾略特": 0,
            "菲妮娅": 0,
            "闻笙": 0,
            "阿知波": 0,
            "隼": 0,
            "雷火": 0,
            "魇": 0,
            "黛丝莉": 0,
        },
        station_level={
            "7号自由港": 17,
            "修格里城": 13,
            "曼德矿场": 12,
            "澄明数据中心": 16,
        },
        negotiate_price={
            "7号自由港": 30,
            "修格里城": 30,
            "曼德矿场": 30,
            "淘金乐园": 30,
            "澄明数据中心": 30,
            "荒原站": 30,
            "铁盟哨站": 30,
            "阿妮塔战备工厂": 30,
            "阿妮塔能源研究所": 30,
        },
        max_goods_num=625,
    )
    LOGGER.info(route)
    print(show(route))
    assert route.city_data[0].profit != 0 and route.city_data[1].profit != 0


def test_get_goods_info_kmou():
    route = get_goods_info_kmou(
        city_book={
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
        },
        skill_level={
            "伊尔": 0,
            "卡洛琳": 0,
            "叶珏": 0,
            "塞西尔": 0,
            "多萝西": 0,
            "奈弥": 0,
            "山岚": 0,
            "星花": 0,
            "朱利安": 2,
            "狮鬃": 0,
            "瑞秋": 0,
            "瓦伦汀": 0,
            "艾略特": 0,
            "菲妮娅": 0,
            "闻笙": 0,
            "阿知波": 0,
            "隼": 0,
            "雷火": 0,
            "魇": 0,
            "黛丝莉": 0,
        },
        station_level={
            "7号自由港": 17,
            "修格里城": 13,
            "曼德矿场": 12,
            "澄明数据中心": 16,
        },
        negotiate_price={
            "7号自由港": 30,
            "修格里城": 30,
            "曼德矿场": 30,
            "淘金乐园": 30,
            "澄明数据中心": 30,
            "荒原站": 30,
            "铁盟哨站": 30,
            "阿妮塔战备工厂": 30,
            "阿妮塔能源研究所": 30,
        },
        max_goods_num=625,
        uuid=cfg.uuid.value,
    )
    LOGGER.info(route)
    print(show(route))
    assert route.city_data[0].profit != 0 and route.city_data[1].profit != 0


if __name__ == "__main__":
    test_get_goods_info_kmou()
    test_get_goods_info_srap()
