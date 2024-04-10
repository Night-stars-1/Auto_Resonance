"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2024-04-10 22:56:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import CheckBox, ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, SettingCardGroup

from ..common.style_sheet import StyleSheet

DAILYTASKS = [
    "今日首次登录",
    "获得5场战斗胜利",
    "完成1个治安任务",
    "在休息区的黑月商店购买1次桦石",
    "成功抬价3次",
    "完成1个商会订单",
    "通过交易赚到20000铁盟币",
    "单笔交易利润达到30000 铁盟币",
    "行驶200KM",
    "行驶300KM",
    "成功砍价1次",
    "成功抬价1次",
    "通过交易赚到50000铁盟币",
    "通过交易赚到100000铁盟币",
]


class DailyTaskInterface(ScrollArea):
    """每日任务 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.settingLabel = QLabel("每日任务", self)

        self.__initWidget()

    def loadSamples(self):
        """load samples"""
        # basic input samples
        self.configGroup = SettingCardGroup("施工中...", self.scrollWidget)

        for daily_task_name in DAILYTASKS:
            self.configGroup.addSettingCard(
                CheckBox(
                    text=daily_task_name,
                    parent=self.configGroup,
                )
            )

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("DailyTaskInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.loadSamples()
        self.__initLayout()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.configGroup)
