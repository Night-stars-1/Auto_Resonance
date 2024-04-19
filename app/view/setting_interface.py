"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-07 23:14:47
LastEditTime: 2024-04-19 13:31:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

# coding:utf-8
from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, SettingCardGroup, SwitchSettingCard

from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..components.settings.line_edit_setting_card import LineEditSettingCard

from core.models.config import config

class SettingInterface(ScrollArea):
    """Setting interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel("设置", self)

        # music folders
        self.musicInThisPCGroup = SettingCardGroup("配置", self.scrollWidget)
        self.goodsTypeCard = SwitchSettingCard(
            FIF.TAG,
            "数据源",
            "On为 KMou，Off为 SRAP",
            configItem=cfg.goodsType,
            parent=self.musicInThisPCGroup,
        )
        self.uuidCard = LineEditSettingCard(
            cfg.uuid,
            "KMou商品请求 UUID",
            FIF.PALETTE,
            "KMou商品请求 UUID",
            parent=self.musicInThisPCGroup,
            isPassword=True,
        )
        self.adbPathCard = LineEditSettingCard(
            cfg.adbPath,
            "ADB路径",
            FIF.PALETTE,
            "ADB程序路径",
            parent=self.musicInThisPCGroup,
        )
        self.adbOrderCard = LineEditSettingCard(
            cfg.adbOrder,
            "ADB地址",
            FIF.PALETTE,
            "ADB地址",
            parent=self.musicInThisPCGroup,
        )
        self.isSpeedCard = SwitchSettingCard(
            FIF.PALETTE,
            "是否自动加速",
            "是否自动使用加速弹丸",
            parent=self.musicInThisPCGroup,
        )
        self.isSpeedCard.setValue(config.global_config.isSpeed)
        self.isSpeedCard.switchButton.checkedChanged.connect(self.__onCheckedChanged)
        self.__initWidget()

    def __onCheckedChanged(self, isChecked: bool):
        config.global_config.isSpeed = isChecked
        config.save_config()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("SettingInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.__initLayout()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.musicInThisPCGroup.addSettingCard(self.goodsTypeCard)
        self.musicInThisPCGroup.addSettingCard(self.uuidCard)
        self.musicInThisPCGroup.addSettingCard(self.adbPathCard)
        self.musicInThisPCGroup.addSettingCard(self.adbOrderCard)
        self.musicInThisPCGroup.addSettingCard(self.isSpeedCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)
