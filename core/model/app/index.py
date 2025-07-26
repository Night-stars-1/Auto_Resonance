"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-09-10 20:22:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field

from core.control.adb_port import EmulatorInfo, EmulatorType
from core.utils.utils import RESOURCES_PATH, read_json

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
APP_PATH = ROOT_PATH / "config" / "app.json"
"""自动程序配置文件路径"""
APP_PATH.parent.mkdir(parents=True, exist_ok=True)
city_sell_data: Dict[str, Dict[str, int]] = read_json(
    RESOURCES_PATH / "goods/CityGoodsSellData.json"
)
CITYS = list(city_sell_data.keys())


class GlobalModel(BaseModel):
    """全局模型"""

    device: EmulatorInfo = EmulatorInfo(
        name="自定义端口", port=16384, path="", type=EmulatorType.CUSTOM, index=0
    )
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
    data = read_json(APP_PATH)
    app = Config.model_validate(data)
