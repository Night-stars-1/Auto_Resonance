"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:57:00
LastEditTime: 2024-05-04 17:23:38
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict

import requests

from core.models import app

from ..goods import SHOP
from ..models.kmou import KMouRequestModel


def get_goods_info():
    url = "https://reso-data.kmou424.moe/api/fetch/goods_info"
    response = requests.get(url, params={"uuid": app.Global.uuid})
    goods_data = KMouRequestModel.model_validate(response.json())
    return SHOP(goods_data).get_optimal_route()
