"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-04-11 20:23:53
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, RootModel


class TargetGoodModel(BaseModel):
    """目标商品模型"""

    class GoodsData(BaseModel):
        """商品数据"""

        num: int
        """数量"""
        price: int
        """价格"""

    goods_data: Dict[str, GoodsData] = {}
    """商品数据"""
    num: int = 0
    """总量"""
    price: int = 0
    """总价"""
    book: int = 0
    """书"""


class RouteModel(BaseModel):
    """路线模型"""

    buy_city_name: str = ""
    """购买城市"""
    sell_city_name: str = ""
    """出售城市"""
    tax_rate: float = 99.9
    """税率"""
    buy_price: int = 0
    """购买总价格"""
    sell_price: int = 0
    """出售总价格"""
    city_tired: int = 999
    """总疲劳"""
    profit: int = 0
    """总利润"""
    tired_profit: int = 0
    """单位利润"""
    book_profit: int = 0
    """单书利润"""
    book: int = 99
    """书"""
    num: int = 0
    """数量"""
    goods_data: Dict[str, TargetGoodModel.GoodsData] = {}
    """商品数据"""


class RoutesModel(RootModel):
    """路线模型集合"""

    root: List[RouteModel] = []
    """路线模型集合"""

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def find(self, **kargs) -> Optional[RouteModel]:
        for i in self.root:
            if all(getattr(i, key) == value for key, value in kargs.items()):
                return i
        return None
