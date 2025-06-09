"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:14:29
LastEditTime: 2025-02-11 19:26:08
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Dict, Literal

from loguru import logger

from auto.run_business.buy import buy_business
from auto.run_business.sell import sell_business
from core.adb.adb import STOP, connect, input_tap, screenshot
from core.image import get_bgr
from core.model import app
from core.model.city_goods import RouteModel, RoutesModel
from core.module.bgr import BGR, BGRGroup
from core.preset import click_station, get_station, go_outlets, wait_gbr
from core.utils.utils import read_json

_city_sell_data: Dict[str, Dict[str, int]] = read_json(
    "resources/goods/CityGoodsSellData.json"
)
city_sell_data = {
    city: dict(sorted(goods.items(), key=lambda item: item[1]["price"], reverse=True))
    for city, goods in _city_sell_data.items()
}


def show(routes: RoutesModel):
    route = routes.city_data
    message = f"""{route[0].buy_city_name}<->{route[0].sell_city_name}:
{route[0].buy_city_name}:
    商品顺序: {"->".join(route[0].goods_data.keys())}
    议价次数: {route[0].haggle_num}
    书本数量: {route[0].book}
{route[0].sell_city_name}:
    商品顺序: {"->".join(route[1].goods_data.keys())}
    议价次数: {route[1].haggle_num}
    书本数量: {route[1].book}"""

    return message


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
            BGRGroup([0, 123, 240], [2, 133, 255]) == bgr
            or BGR(225, 225, 225) == bgr
            or BGRGroup([0, 170, 240], [5, 185, 255]) == bgr
        ):
            return True
        else:
            logger.error("进入交易所失败")
            return False
    else:
        logger.error("进入交易所失败")
        return False


def run(routes: RoutesModel):
    logger.info(show(routes))
    status = connect()
    if not status:
        logger.error("ADB连接失败")
        return False
    city_name = get_station()
    if routes.city_data[0].sell_city_name == city_name:
        routes.city_data = [routes.city_data[1], routes.city_data[0]]
    for city in routes.city_data:
        logger.info(f"{city.buy_city_name}->{city.sell_city_name}")
        click_station(city.buy_city_name, cur_station=city_name).wait()
        go_business("buy")
        goods_data = list(city.goods_data.keys())
        buy_business(
            goods_data[:1],
            goods_data[1:],
            city.haggle_num,
            max_book=city.book,
        )
        click_station(city.sell_city_name, cur_station=city_name).wait()
        go_business("sell")
        sell_business(city.haggle_num)
        # 流程跑完，更改站点名称为当前出售商品的站点
        city_name = city.sell_city_name
    logger.info("运行完成")
    return True


def two_city_run(buy_city_name: str, sell_city_name: str):
    global STOP
    STOP = False
    count = app.RunBuy.BuyCount
    buy_haggle_num = app.CityHaggle[buy_city_name]
    sell_haggle_num = app.CityHaggle[sell_city_name]
    buy_book_num = app.CityBook[buy_city_name]
    sell_book_num = app.CityBook[sell_city_name]
    routes = RoutesModel(
        city_data=[
            RouteModel(
                buy_city_name=buy_city_name,
                sell_city_name=sell_city_name,
                haggle_num=buy_haggle_num,
                book=buy_book_num,
                goods_data=city_sell_data[buy_city_name],
            ),
            RouteModel(
                buy_city_name=sell_city_name,
                sell_city_name=buy_city_name,
                haggle_num=sell_haggle_num,
                book=sell_book_num,
                goods_data=city_sell_data[sell_city_name],
            ),
        ],
    )
    logger.info(f"准备运行端点跑商，运行次数: {count}")
    for i in range(count):
        if not run(routes) or STOP:
            break


def stop():
    """
    说明:
        停止运行
    """
    global STOP
    STOP = True
