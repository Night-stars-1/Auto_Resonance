"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:57:00
LastEditTime: 2024-04-14 02:56:41
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict

import requests

from core.models.city_goods import SkillLevelModel

from ..models.kmou import KMouRequestModel
from .shop import SHOP


def get_goods_info(
    city_book: Dict[str, int],
    skill_level: Dict[str, int],
    station_level: Dict[str, int],
    city_tired: Dict[str, int],
    max_goods_num: int,
    uuid: str,
):
    url = "https://reso-data.kmou424.moe/api/fetch/goods_info"
    response = requests.get(url, params={"uuid": uuid})
    data = KMouRequestModel.model_validate(response.json())
    return SHOP(
        data, city_book, skill_level, station_level, city_tired, max_goods_num
    ).get_optimal_route()
