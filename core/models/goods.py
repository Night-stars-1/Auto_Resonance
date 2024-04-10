"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-04-09 22:05:48
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field, RootModel

from .city_data import city_goods


class GoodModel(BaseModel):
    """商品模型"""

    name: str
    """名称"""
    city: str
    """城市"""
    type: str
    """类型"""
    num: int = 0
    """数量"""
    price: int
    """价格"""
    base_price: int
    """基础价格"""

    def __init__(self, **data: Any) -> None:
        if "station" in data:
            data["city"] = data.pop("station")
        super().__init__(**data)


class GoodsModel(BaseModel):
    """商品列表模型"""

    goods: List[GoodModel]
    buy_goods: Dict[str, Dict[str, GoodModel]] = {}
    sell_goods: Dict[str, Dict[str, GoodModel]] = {}
    speciality_goods: Dict[str, Dict[str, GoodModel]] = {}

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.set_goods()

    def set_goods(self) -> None:
        """设置商品"""
        for good in self.goods:
            if good.city not in city_goods:
                continue
            if good.type == "buy":
                city_good_data = city_goods[good.city][good.name]
                good.num = city_good_data.num
                self.buy_goods.setdefault(good.city, {}).setdefault(good.name, good)
                if city_good_data.isSpeciality:
                    self.speciality_goods.setdefault(good.city, {}).setdefault(
                        good.name, good
                    )
            elif good.type == "sell":
                self.sell_goods.setdefault(good.city, {}).setdefault(good.name, good)

    def find(self, **kargs) -> List[GoodModel]:
        data = []
        for i in self.goods:
            for key, value in kargs.items():
                if getattr(i, key) == value:
                    data.append(i)
        return data
