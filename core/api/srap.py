"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:57:00
LastEditTime: 2024-04-20 22:58:34
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import gzip
from typing import Dict, Union

import orjson
import requests

from ..goods import SHOP
from ..models.srap import SrapRequestGzipModel


def get_goods_info():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }

    json_data = {
        "station_name": "all",
        "gzip": True,
    }

    response = requests.post(
        "https://goda.srap.link/getGoods", headers=headers, json=json_data
    )
    if response.status_code != 200:
        raise Exception(f"请求失败: {response.text}")
    result = gzip.decompress(response.content).decode("utf-8")
    goods_data = SrapRequestGzipModel.model_validate(orjson.loads(result))
    return SHOP(goods_data).get_optimal_route()


def get_boss():
    try:
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        }

        response = requests.post("https://goda.srap.link/getBoss", headers=headers)
        data: Dict[str, Union[str, int]] = response.json()["data"]
        return [
            {
                "title": f"{value['name']}-{value['curr_index']}",
                "content": key,
                "progress": value["ratio"],
            }
            for key, value in data.items()
        ]
    except Exception:
        return []
