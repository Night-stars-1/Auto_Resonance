"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:57:00
LastEditTime: 2024-04-10 00:19:37
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import requests

from ..models.kmou import KMouRequestModel
from .shop import SHOP


def get_goods_info(uuid: str) -> KMouRequestModel:
    url = "https://reso-data.kmou424.moe/api/fetch/goods_info"
    response = requests.get(url, params={"uuid": uuid})
    data = KMouRequestModel.model_validate(response.json())
    return SHOP(data).get_go_back_optimal_route_by_tired_profit()
