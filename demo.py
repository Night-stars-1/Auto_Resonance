"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:56:16
LastEditTime: 2024-04-12 22:56:52
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
from core.presets import click_station, get_city, go_home


def run(city_config: dict = {}):
    connect()
    route = get_goods_info(city_config)
    city_name = get_city()
    if route.city_data[0].sell_city_name == city_name:
        route.city_data = [route.city_data[1], route.city_data[0]]
        # print(route.city_data)
    for city in route.city_data:
        logger.info(f"{city.buy_city_name}->{city.sell_city_name}")
        go_home()
        click_station(city.buy_city_name).wait()
        go_business("buy")
        buy_business(
            city.buy_goods + list(city.normal_goods.keys()), 20, max_book=city.book
        )
        go_home()
        click_station(city.sell_city_name).wait()
        go_business("sell")
        sell_business()
    logger.info("运行完成")

if __name__ == "__main__":
    run(
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
    # click_station("修格里城")
