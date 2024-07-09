"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-06-13 16:17:25
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
APP_PATH = ROOT_PATH / "config" / "app.json"
"""自动程序配置文件路径"""
APP_PATH.parent.exists() or APP_PATH.parent.mkdir(parents=True, exist_ok=True)


class RestAreaModel(BaseModel):
    """休息区模型"""

    class RunTimeModel(BaseModel):
        runtime: float = 0.0
        """运行时间"""

    huashi: RunTimeModel = RunTimeModel()
    """桦石"""


class GlobalModel(BaseModel):
    """全局模型"""

    adbOrder: str = ""
    """ADB Order"""
    adbPath: str = ""
    """ADB 路径"""
    goodsType: bool = False
    """货物类型"""
    uuid: str = ""


class NegotiatePriceModel(BaseModel):
    """议价模型"""

    buyTired: int = 10
    """买入疲劳值"""
    sellTired: int = 10
    """卖出疲劳值"""
    七号自由港: int = Field(2, alias="7号自由港")
    """七号自由港"""
    修格里城: int = 2
    """修格里城"""
    曼德矿场: int = 2
    """曼德矿场"""
    淘金乐园: int = 2
    """淘金乐园"""
    澄明数据中心: int = 2
    """澄明数据中心"""
    荒原站: int = 2
    """荒原站"""
    铁盟哨站: int = 2
    """铁盟哨站"""
    阿妮塔发射中心: int = 2
    """阿妮塔发射中心"""
    阿妮塔战备工厂: int = 2
    """阿妮塔战备工厂"""
    阿妮塔能源研究所: int = 2
    """阿妮塔能源研究所"""

    def get_tired(self, station_name: str, default: int) -> int:
        """获取疲劳值"""
        return self.model_dump(by_alias=True).get(station_name, default)


class RunningBusinessModel(BaseModel):
    """跑商模型"""

    maxGoodsNum: int = 625
    """最大货物数量"""
    priceThreshold: int = 1000
    """价格阈值"""
    profitThreshold: int = 160000
    """利润阈值"""
    totalMaxBook: int = 4
    """总最大预定"""
    tiredProfitThreshold: int = 12000
    """单位疲劳阈值"""


class StationLevelModel(BaseModel):
    """站点等级模型"""

    七号自由港: int = Field(19, alias="7号自由港")
    """七号自由港"""
    修格里城: int = 13
    """修格里城"""
    曼德矿场: int = 14
    """曼德矿场"""
    澄明数据中心: int = 17
    """澄明数据中心"""
    阿妮塔发射中心: int = 0
    """阿妮塔发射中心"""


class Config(BaseModel):
    """自动程序配置"""

    Global: GlobalModel = GlobalModel()
    """全局"""
    NegotiatePrice: NegotiatePriceModel = NegotiatePriceModel()
    """议价"""
    RunningBusiness: RunningBusinessModel = RunningBusinessModel()
    """跑商"""
    StationLevel: Dict[str, int] = {}
    """城市声望等级"""
    SkillLevel: Dict[str, int] = {}
    """角色共振等级"""


if APP_PATH.exists() and APP_PATH.is_file():
    with open(APP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    app = Config.model_validate(data)
