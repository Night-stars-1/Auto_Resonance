"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-05-11 22:12:26
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Any, Dict, List

from loguru import logger
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
    profit: int = 0
    """利润"""
    base_price: int
    """基础价格"""
    isSpeciality: bool = False
    """是否特产"""

    def __init__(self, **data: Any) -> None:
        if "station" in data:
            data["city"] = data.pop("station")
        super().__init__(**data)


class GoodInfoModel(BaseModel):
    """商品信息模型"""

    name: str
    """名称"""
    buy_price: int
    """购买价格"""
    sell_price: int
    """出售价格"""
    profit: int
    """利润"""
    buy_num: int
    """购买数量"""


LACK_DATA = []


class GoodsModel(BaseModel):
    """商品列表模型"""

    goods: List[GoodModel]
    """商品列表"""
    buy_goods: Dict[str, Dict[str, GoodModel]] = {}
    """城市可购买的商品信息"""
    sell_goods: Dict[str, Dict[str, GoodModel]] = {}
    """城市可出售的商品信息"""
    speciality_goods: Dict[str, Dict[str, GoodModel]] = {}
    """城市可购买的特产商品信息"""

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.set_goods()

    def set_goods(self) -> None:
        """设置商品"""
        for good in self.goods:
            if good.city not in city_goods:
                if good.city not in LACK_DATA:
                    LACK_DATA.append(good.city)
                    logger.error(f"{good.city} 数据不存在")
                continue
            if good.type == "buy":
                if good.name in city_goods[good.city]:
                    city_good_data = city_goods[good.city][good.name]
                    good.num = city_good_data.num
                    good.isSpeciality = city_good_data.isSpeciality
                    self.buy_goods.setdefault(good.city, {}).setdefault(good.name, good)
                    if city_good_data.isSpeciality:
                        self.speciality_goods.setdefault(good.city, {}).setdefault(
                            good.name, good
                        )
                else:
                    logger.error(f"{good.city}不存在{good.name}")
            elif good.type == "sell":
                self.sell_goods.setdefault(good.city, {}).setdefault(good.name, good)

    def find(self, **kargs) -> List[GoodModel]:
        data = []
        for i in self.goods:
            if all(getattr(i, key) == value for key, value in kargs.items()):
                data.append(i)
        return data
