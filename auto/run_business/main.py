"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:14:29
LastEditTime: 2024-04-28 22:33:46
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Literal

from loguru import logger

from core.adb import connect, input_tap, screenshot
from core.api.kmou import get_goods_info as get_goods_info_kmou
from core.api.srap import get_goods_info as get_goods_info_srap
from core.image import get_bgr
from core.models.city_goods import RoutesModel
from core.module.bgr import BGR
from core.presets import click_station, get_city, go_home, go_outlets, wait_gbr
from core.utils import compare_ranges

from .buy import buy_business
from .sell import sell_business


def go_business(type: Literal["buy", "sell"] = "buy"):
    result = go_outlets("交易所")
    is_join = wait_gbr(
        pos=(286, 35),
        min_gbr=[250, 250, 250],
        max_gbr=[255, 255, 255],
        cropped_pos1=(242, 11),
        cropped_pos2=(414, 66),
    )
    if result and is_join:
        if type == "buy":
            input_tap((927, 321))
        elif type == "sell":
            input_tap((932, 404))
        time.sleep(1.0)
        bgr = get_bgr(screenshot(), (1175, 460))
        logger.debug(f"进入交易所颜色检查: {bgr}")
        if (
            bgr == [2, 133, 253]
            or bgr == [0, 183, 253]
            or BGR(225, 225, 225) == bgr
        ):
            return True
        else:
            logger.error("进入交易所失败")
            return False
    else:
        logger.error("进入交易所失败")
        return False


def run(
    order: str,
    path: str,
    route: RoutesModel,
):
    status = connect(order, path)
    if not status:
        logger.error("ADB连接失败")
        return False
    city_name = get_city()
    if route.city_data[0].sell_city_name == city_name:
        route.city_data = [route.city_data[1], route.city_data[0]]
        # print(route.city_data)
    for city in route.city_data:
        if city.profit == 0:
            logger.info("没有数据")
            return False
        logger.info(f"{city.buy_city_name}->{city.sell_city_name}")
        go_home()
        click_station(city.buy_city_name).wait()
        go_business("buy")
        buy_business(
            city.primary_goods,
            city.secondary_goods,
            city.buy_argaining_num,
            max_book=city.book,
        )
        go_home()
        click_station(city.sell_city_name).wait()
        go_business("sell")
        sell_business(city.sell_argaining_num)
    logger.info("运行完成")
    return True
