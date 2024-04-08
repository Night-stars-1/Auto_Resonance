"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-04-08 22:32:19
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import List

from pydantic import BaseModel

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
CONFIG_PATH = ROOT_PATH / "config.json"
"""自动程序配置文件路径"""


class RestAreaModel(BaseModel):
    """休息区模型"""


class RSBModel(BaseModel):
    """铁安局模型"""

    city: str = "7号自由港"
    """刷取城市"""
    levelSerialPos: List[int] = "1"
    """刷取关卡序号位置"""
    name: str = "所有"
    """刷取关卡名称 所有为全部刷取"""


class Config(BaseModel):
    """自动程序配置"""

    version: str = "1.0.0"
    """版本号"""
    rsb: RSBModel = RSBModel()
    """铁安局配置"""
