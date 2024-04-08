"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:18:17
LastEditTime: 2024-04-08 22:43:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, RootModel


class GoodModel(BaseModel):
    """商品模型"""

    id: str
    """ID"""
    name: str
    """名称"""
    station: str
    """城市"""
    stock: int
    """库存"""
    type: str
    """类型"""
    base_price: int
    """基础价格"""
    price: int
    """价格"""
    next_trend: int
    """下一个趋势"""
    update_time: datetime
    """更新时间"""
    update_timestamp: int
    """更新时间戳"""


class KMouRequestModel(RootModel):
    root: List[GoodModel]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    @property
    def items(self) -> List[GoodModel]:
        return self.root


data = KMouRequestModel.model_validate(
    [
        {
            "id": "a482e1d65d84",
            "name": "阿妮塔101民用无人机",
            "station": "7号自由港",
            "stock": 14,
            "type": "buy",
            "base_price": 1659,
            "price": 1709,
            "next_trend": 1,
            "update_time": "2024-04-08 13:40:23",
            "update_timestamp": 1712583623,
        },
    ]
)
for i in data.items:
    print(i.name, i.stock)
    print(i.update_timestamp)
    print(datetime.fromtimestamp(i.update_timestamp))
    print(i.update_time)
    print()
