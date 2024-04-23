"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:18:17
LastEditTime: 2024-04-14 20:50:30
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from itertools import chain
from typing import Any, Dict, List

from .goods import GoodModel, GoodsModel


class SrapRequestModel(GoodsModel):
    """SRAP请求模型"""

    status: bool
    """状态"""
    message: str
    """消息"""
    data: Dict[str, List[GoodModel]]
    """商品数据"""

    def __init__(self, **data) -> None:
        data["goods"] = list(chain.from_iterable(data["data"].values()))
        super().__init__(**data)


class SrapRequestGzipModel(GoodsModel):
    """SRAP请求模型"""

    def __init__(self, **data) -> None:
        data["goods"] = list(chain.from_iterable(data.values()))
        super().__init__(**data)
