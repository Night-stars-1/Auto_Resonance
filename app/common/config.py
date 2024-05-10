"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:13:20
LastEditTime: 2024-05-10 23:32:54
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

# coding:utf-8
import sys
from enum import Enum
from typing import List

from PyQt5.QtCore import QLocale
from qfluentwidgets import (
    BoolValidator,
    ConfigItem,
    ConfigSerializer,
    OptionsConfigItem,
    OptionsValidator,
    Theme,
    qconfig,
)

from version import __version__

from .running_business_config import RunningBusinessConfig


class Language(Enum):
    """Language enumeration"""

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """Language serializer"""

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


class Config(RunningBusinessConfig):
    """Config of application"""

    # uuid
    uuid = ConfigItem("Global", "uuid", "", None)
    goodsType = ConfigItem("Global", "goodsType", False, BoolValidator())
    adbPath = ConfigItem("Global", "adbPath", "resources\\lib\\adb", None)
    adbOrder = ConfigItem("Global", "adbOrder", "127.0.0.1:7555", None)

    # 我建我路
    thisRoadThatBoss = ConfigItem("ThisRoadThat", "boss", 10, None)
    thisRoadThatAttackOne = ConfigItem(
        "ThisRoadThat", "attack_one", False, BoolValidator()
    )
    thisRoadThatAttackTwo = ConfigItem(
        "ThisRoadThat", "attack_two", False, BoolValidator()
    )
    thisRoadThatAttackThree = ConfigItem(
        "ThisRoadThat", "attack_three", False, BoolValidator()
    )
    thisRoadThatAttackFour = ConfigItem(
        "ThisRoadThat", "attack_four", False, BoolValidator()
    )
    thisRoadThatAttackFive = ConfigItem(
        "ThisRoadThat", "attack_five", False, BoolValidator()
    )
    thisRoadThatTransportOrder = ConfigItem("ThisRoadThat", "thisRoadThat", 1, None)

    # task
    huashi = ConfigItem("Task", "huashi", False, BoolValidator())  # 购买桦石
    railwaySafetyBureau = ConfigItem(
        "Task", "railway_safety_bureau", False, BoolValidator()
    )  # 铁安局
    runBusiness = ConfigItem("Task", "run_business", False, BoolValidator())  # 自动跑商

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )

YEAR = 2023
AUTHOR = "Night-stars-1"
VERSION = __version__
REPO_URL = "https://github.com/Night-stars-1/Auto_Resonance"


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load("config/app.json", cfg)
