"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:13:20
LastEditTime: 2024-04-08 00:19:18
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

# coding:utf-8
import sys
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (
    BoolValidator,
    ConfigItem,
    ConfigSerializer,
    OptionsConfigItem,
    OptionsValidator,
    QConfig,
    Theme,
    __version__,
    qconfig,
)

from core import adb


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


class Config(QConfig):
    """Config of application"""

    # uuid
    uuid = ConfigItem("Global", "uuid", "", None)
    goodsType = ConfigItem("Global", "goodsType", False, BoolValidator())
    adbPath = ConfigItem("Global", "adbPath", "resources\\lib\\adb", None)
    adbOrder = ConfigItem("Global", "adbOrder", "127.0.0.1:7555", None)

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
AUTHOR = "zhiyiYo"
VERSION = __version__
REPO_URL = "https://github.com/Night-stars-1/Auto_Resonance"


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load("app/config/config.json", cfg)
