"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:57:00
LastEditTime: 2024-04-12 12:55:55
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict

import requests

from ..models.srap import SrapRequestModel
from .shop import SHOP


def get_goods_info(
    city_book: Dict[str, int],
    skill_level: Dict[str, int],
    station_level: Dict[str, int],
    max_goods_num: int,
    _=None,
):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }

    json_data = {
        "station_name": "all",
    }

    response = requests.post(
        "https://goda.srap.link/getGoods", headers=headers, json=json_data
    )
    data = SrapRequestModel.model_validate(response.json())
    return SHOP(
        data, city_book, skill_level, station_level, max_goods_num
    ).get_optimal_route()
