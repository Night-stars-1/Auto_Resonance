"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-09-10 20:22:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field

from core.utils.utils import read_json

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
APP_PATH = ROOT_PATH / "config" / "app.json"
"""自动程序配置文件路径"""
APP_PATH.parent.exists() or APP_PATH.parent.mkdir(parents=True, exist_ok=True)
city_sell_data: Dict[str, Dict[str, int]] = read_json(
    "resources/goods/CityGoodsSellData.json"
)
CITYS = list(city_sell_data.keys())


class GlobalModel(BaseModel):
    """全局模型"""

    adbOrder: str = ""
    """ADB Order"""
    adbPort: str = ""
    """ADB 端口"""
    adbPath: str = ""
    """ADB 路径"""
    emulatorType: str = ""
    """模拟器类型"""
    goodsType: bool = False
    """货物类型"""
    uuid: str = ""
    mirrorCdk: str = ""
    """Mirror酱CDK"""

class RunBuyModel(BaseModel):
    """进货"""

    BuyCount: int = 0
    """运行次数"""

class Config(BaseModel):
    """自动程序配置"""

    Global: GlobalModel = GlobalModel()
    """全局"""
    CityBook: dict = Field(default_factory=lambda: {city: 0 for city in CITYS})
    """进货书"""
    CityHaggle: dict = Field(default_factory=lambda: {city: 0 for city in CITYS})
    """议价"""
    RunBuy: RunBuyModel = RunBuyModel()
    """跑商配置"""

if APP_PATH.exists() and APP_PATH.is_file():
    with open(APP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    app = Config.model_validate(data)
