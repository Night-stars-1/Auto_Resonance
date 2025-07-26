"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:13:20
LastEditTime: 2024-05-10 23:32:54
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys

from qfluentwidgets import ConfigItem, QConfig, Theme, qconfig, ConfigSerializer

from app.utils.config import CITYS
from core.control.adb_port import EmulatorInfo, EmulatorType
from version import __version__


class RunningBusinessConfig(QConfig):
    """Config of application"""

    BuyCount = ConfigItem("RunBuy", "BuyCount", 0, None)

    for city in CITYS:
        # 特殊适配7号自由港
        locals()[f"{city}进货书"] = ConfigItem(
            "CityBook", city.replace("七号自由港", "7号自由港"), 0, None
        )
        locals()[f"{city}议价次数"] = ConfigItem(
            "CityHaggle", city.replace("七号自由港", "7号自由港"), 0, None
        )


def isWin11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000

class EmulatorSerializer(ConfigSerializer):
    def serialize(self, value: EmulatorInfo) -> dict:
        return value.to_dict()

    def deserialize(self, data: dict) -> EmulatorInfo:
        return EmulatorInfo.from_dict(data)

class Config(RunningBusinessConfig):
    """Config of application"""

    emulatorType = ConfigItem("Global", "emulatorType", "Auto", None)
    device = ConfigItem(
        "Global",
        "device",
        EmulatorInfo(name="自定义端口", port=16384, path="", type=EmulatorType.CUSTOM, index=0),
        serializer=EmulatorSerializer(),
    )

    # Mirror酱
    mirrorCdk = ConfigItem("Global", "mirrorCdk", "", None)


YEAR = 2023
AUTHOR = "Night-stars-1"
VERSION = __version__
REPO_URL = "https://github.com/Night-stars-1/Auto_Resonance"


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load("config/app.json", cfg)
