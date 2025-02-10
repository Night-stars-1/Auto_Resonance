"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:14:29
LastEditTime: 2025-02-04 23:41:51
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Dict, Literal

from loguru import logger

from auto.run_business.buy import buy_business
from auto.run_business.sell import sell_business
from core.adb.adb import STOP, connect, input_tap, screenshot
from core.api.kmou import get_goods_info as get_goods_info_kmou
from core.api.srap import get_goods_info as get_goods_info_srap
from core.exceptions import StopExecution
from core.goods import show
from core.image import get_bgr
from core.model import app
from core.model.city_goods import RouteModel, RoutesModel
from core.module.bgr import BGR, BGRGroup
from core.preset import click_station, get_city, go_home, go_outlets, wait_gbr
from core.utils import read_json

_city_sell_data: Dict[str, Dict[str, int]] = read_json(
    "resources/goods/CityGoodsSellData.json"
)
city_sell_data = {
    city: dict(sorted(goods.items(), key=lambda item: not item[1]["price"]))
    for city, goods in _city_sell_data.items()
}


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
    city_name = get_city()
    if routes.city_data[0].sell_city_name == city_name:
        routes.city_data = [routes.city_data[1], routes.city_data[0]]
    for city in routes.city_data:
        if city.profit == 0:
            logger.info("没有数据")
            return False
        logger.info(f"{city.buy_city_name}->{city.sell_city_name}")
        go_home()
        click_station(city.buy_city_name).wait()
        go_business("buy")
        goods_data = list(city.goods_data.keys())
        buy_business(
            goods_data[:1],
            goods_data[1:],
            city.buy_argaining_num,
            max_book=city.book,
        )
        go_home()
        click_station(city.sell_city_name).wait()
        go_business("sell")
        sell_business(city.sell_argaining_num)
    logger.info("运行完成")
    return True


def two_city_run(buy_city_name: str, sell_city_name: str):
    routes = RoutesModel(
        city_data=[
            RouteModel(
                buy_city_name=buy_city_name,
                buy_argaining_num=4,
                sell_city_name=sell_city_name,
                sell_argaining_num=4,
                book=2,
                profit=-999,  # 无需构建
                goods_data=city_sell_data[buy_city_name],
            ),
            RouteModel(
                buy_city_name=sell_city_name,
                buy_argaining_num=4,
                sell_city_name=buy_city_name,
                sell_argaining_num=4,
                book=2,
                profit=-999,  # 无需构建
                goods_data=city_sell_data[sell_city_name],
            ),
        ],
        profit=-999,  # 无需构建
        tired_profit=0,  # 无需构建
        book_profit=0,  # 无需构建
        book=0,  # 无需构建
    )
    logger.info("当前为端点跑商，下方输出的内容为假信息")
    run(routes)


def stop():
    """
    说明:
        停止运行
    """
    global STOP
    STOP = True


def start():
    """
    说明:
        循环监听单位疲劳利润，达到阈值时进行跑商
    """
    global STOP
    STOP = False
    while True:
        if STOP:
            raise StopExecution()
        if app.Global.goodsType:
            routes = get_goods_info_kmou()
        else:
            routes = get_goods_info_srap()
        if routes.tired_profit >= app.RunningBusiness.tiredProfitThreshold:
            run(routes)
        else:
            logger.info(
                f"疲劳利润: {routes.tired_profit} 阈值: {app.RunningBusiness.tiredProfitThreshold}，未达到阈值不跑商"
            )
            time.sleep(5)


if __name__ == "__main__":
    start()
