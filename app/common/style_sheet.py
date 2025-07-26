"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:13:20
LastEditTime: 2024-04-21 20:04:32
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from enum import Enum

from loguru import logger
from qfluentwidgets import StyleSheetBase, Theme, qconfig

from app.utils.constants import QSS_PATH


class StyleSheet(StyleSheetBase, Enum):
    """Style sheet"""

    LINK_CARD = "link_card"
    SAMPLE_CARD = "sample_card"
    HOME_INTERFACE = "home_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return str(QSS_PATH / f"{theme.value.lower()}/{self.value}.qss")
