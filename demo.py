"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:56:16
LastEditTime: 2024-04-12 00:19:08
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger

from auto.run_business import (
    buy_business,
    click_bargain_button,
    go_business,
    sell_business,
)
from core.adb import connect
from core.goods.srap import get_goods_info
from core.presets import click_station, go_home


def run(**kargs):
    connect()
    click_station("阿妮塔能源研究所")
    go_route, back_route, _ = get_goods_info()
    logger.info(f"{go_route.buy_city_name}<->{go_route.sell_city_name}")
    go_home()
    go_business("buy")
    buy_business(list(back_route.goods_data.keys()), 20)
    go_home()
    click_station(back_route.sell_city_name).wait()
    go_business("sell")
    sell_business()
    go_home()
    click_station(go_route.buy_city_name).wait()
    go_business("buy")
    buy_business(list(go_route.goods_data.keys()), 20)
    go_home()
    click_station(go_route.sell_city_name).wait()
    go_business("sell")
    sell_business()
    go_home()


if __name__ == "__main__":
    run()
    # click_station("修格里城")
