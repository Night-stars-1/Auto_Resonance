# coding:utf-8
from qfluentwidgets import SettingCardGroup, ScrollArea, ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget, QLabel

from app.components.line_edit_setting_card import LineEditSettingCard

from ..common.config import cfg
from ..common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel("设置", self)

        # music folders
        self.musicInThisPCGroup = SettingCardGroup(
            "配置", self.scrollWidget)
        self.uuidCard = LineEditSettingCard(
            cfg.uuid,
            "商品请求 UUID",
            FIF.PALETTE,
            "商品请求 UUID",
            parent=self.musicInThisPCGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.__initLayout()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.musicInThisPCGroup.addSettingCard(self.uuidCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)

