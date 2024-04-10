"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:57:00
LastEditTime: 2024-04-10 00:19:37
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import requests

from ..models.srap import SrapRequestModel
from .shop import SHOP


def get_goods_info():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }

    json_data = {
        'station_name': 'all',
    }

    response = requests.post('https://goda.srap.link/getGoods', headers=headers, json=json_data)
    data = SrapRequestModel.model_validate(response.json())
    return SHOP(data).get_go_back_optimal_route_by_tired_profit()