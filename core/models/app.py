"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-05-04 17:50:35
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from pathlib import Path
from typing import Dict

from pydantic import BaseModel
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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
    七号自由港: int = 2
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


class StationLevelModel(BaseModel):
    """站点等级模型"""

    七号自由港: int = 19
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


class FileHandler(FileSystemEventHandler):
    """监听文本改动"""
    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path

    @property
    def get_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def on_modified(self, event):
        if not event.is_directory and event.src_path == str(self.file_path):
            app.model_validate(self.get_data)


# 创建文件系统事件处理器
event_handler = FileHandler(APP_PATH)

# 创建观察者对象
observer = Observer()
observer.schedule(event_handler, path=APP_PATH.parent, recursive=False)

# 启动观察者
observer.start()
