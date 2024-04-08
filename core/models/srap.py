"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:18:17
LastEditTime: 2024-04-08 22:30:37
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import List, Dict

from pydantic import BaseModel


class GoodModel(BaseModel):
    """商品模型"""

    name: str
    """名称"""
    city: str
    """城市"""
    type: str
    """类型"""
    trend: str
    """趋势"""
    price: int
    """价格"""
    base_price: int
    """基础价格"""
    ratio: int
    """比率"""
    updatedAt: int
    """更新时间"""


class SrapRequestModel(BaseModel):
    """SRAP请求模型"""

    status: bool
    """状态"""
    message: str
    """消息"""
    data: Dict[str, List[GoodModel]]
    """商品数据"""
