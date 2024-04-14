"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 19:53:49
LastEditTime: 2024-04-14 00:11:12
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import ExpandSettingCard, OptionsSettingCard
from qfluentwidgets import FluentIcon as FIF

from app.common.config import qconfig
from app.components.settings.options_setting_card import OptionsSettingCard

if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = OptionsSettingCard(
        qconfig.themeMode,
        FIF.BRUSH,
        "应用主题",
        "调整你的应用外观",
        texts=["浅色", "深色", "跟随系统设置"],
    )
    w.show()
    app.exec_()
