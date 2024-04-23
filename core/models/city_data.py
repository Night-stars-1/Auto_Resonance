"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-09 19:02:29
LastEditTime: 2024-04-09 19:09:30
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field, RootModel

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
RESOURCES_PATH = ROOT_PATH / "resources"
GOODSDATA_PATH = RESOURCES_PATH / "goods" / "CityGoodsData.json"
"""自动程序配置文件路径"""
with open(GOODSDATA_PATH, "r", encoding="utf-8") as f:
    goods_data = json.load(f)


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
