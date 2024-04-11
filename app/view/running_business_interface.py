"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2024-04-11 21:45:09
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import CheckBox, ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, SettingCardGroup

from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..components.settings.line_edit_setting_card import LineEditSettingCard


class RunningBusinessInterface(ScrollArea):
    """每日任务 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.settingLabel = QLabel("跑商配置", self)

        self.__initWidget()

    def loadSamples(self):
        """load samples"""
        # basic input samples
        self.configGroup = SettingCardGroup("进货书设置", self.scrollWidget)

        self.七号自由港 = LineEditSettingCard(
            cfg.七号自由港,
            "七号自由港单次最大进货书",
            FIF.ACCEPT,
            "七号自由港",
            parent=self.configGroup,
        )
        self.澄明数据中心 = LineEditSettingCard(
            cfg.澄明数据中心,
            "澄明数据中心单次最大进货书",
            FIF.ACCEPT,
            "澄明数据中心",
            parent=self.configGroup,
        )
        self.阿妮塔战备工厂 = LineEditSettingCard(
            cfg.阿妮塔战备工厂,
            "阿妮塔战备工厂单次最大进货书",
            FIF.ACCEPT,
            "阿妮塔战备工厂",
            parent=self.configGroup,
        )
        self.阿妮塔能源研究所 = LineEditSettingCard(
            cfg.阿妮塔能源研究所,
            "阿妮塔能源研究所单次最大进货书",
            FIF.ACCEPT,
            "阿妮塔能源研究所",
            parent=self.configGroup,
        )
        self.淘金乐园 = LineEditSettingCard(
            cfg.淘金乐园,
            "淘金乐园单次最大进货书",
            FIF.ACCEPT,
            "淘金乐园",
            parent=self.configGroup,
        )
        self.曼德矿场 = LineEditSettingCard(
            cfg.曼德矿场,
            "曼德矿场单次最大进货书",
            FIF.ACCEPT,
            "曼德矿场",
            parent=self.configGroup,
        )
        self.荒原站 = LineEditSettingCard(
            cfg.荒原站,
            "荒原站单次最大进货书",
            FIF.ACCEPT,
            "荒原站",
            parent=self.configGroup,
        )
        self.铁盟哨站 = LineEditSettingCard(
            cfg.铁盟哨站,
            "铁盟哨站单次最大进货书",
            FIF.ACCEPT,
            "铁盟哨站",
            parent=self.configGroup,
        )
        self.修格里城 = LineEditSettingCard(
            cfg.修格里城,
            "修格里城单次最大进货书",
            FIF.ACCEPT,
            "修格里城",
            parent=self.configGroup,
        )

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("RunningBusinessInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.loadSamples()
        self.__initLayout()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.configGroup.addSettingCard(self.七号自由港)
        self.configGroup.addSettingCard(self.澄明数据中心)
        self.configGroup.addSettingCard(self.阿妮塔战备工厂)
        self.configGroup.addSettingCard(self.阿妮塔能源研究所)
        self.configGroup.addSettingCard(self.淘金乐园)
        self.configGroup.addSettingCard(self.曼德矿场)
        self.configGroup.addSettingCard(self.荒原站)
        self.configGroup.addSettingCard(self.铁盟哨站)
        self.configGroup.addSettingCard(self.修格里城)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.configGroup)
