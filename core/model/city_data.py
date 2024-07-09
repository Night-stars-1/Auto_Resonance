"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-09 19:02:29
LastEditTime: 2024-07-09 15:51:12
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict

from pydantic import BaseModel, RootModel

from core.utils import read_json, RESOURCES_PATH

GOODSDATA_PATH = RESOURCES_PATH / "goods" / "CityGoodsData.json"
"""自动程序配置文件路径"""
goods_data = read_json(GOODSDATA_PATH)


class CityGoodsDataModel(BaseModel):
    """商品模型"""

    isSpeciality: bool
    """是否特产"""
    num: int


class CityGoodsModel(RootModel):
    root: Dict[str, Dict[str, CityGoodsDataModel]]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


city_goods = CityGoodsModel.model_validate(goods_data)
