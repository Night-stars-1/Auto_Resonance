# coding:utf-8
from qfluentwidgets import SettingCardGroup, ScrollArea, ExpandLayout, PrimaryPushSettingCard, InfoBar, InfoBarPosition, SwitchSettingCard
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget, QLabel

from app.components.line_edit_setting_card import LineEditSettingCard

from ..common.config import cfg
from ..common.style_sheet import StyleSheet

from core.goods.kmou import get_goods_info as get_goods_info_kmou
from core.goods.srap import get_goods_info as get_goods_info_srap

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
        self.goodsTypeCard = SwitchSettingCard(
            FIF.TAG,
            "数据源",
            "On为 KMou，Off为 SRAP",
            configItem=cfg.goodsType,
            parent=self.musicInThisPCGroup
        )
        self.uuidCard = LineEditSettingCard(
            cfg.uuid,
            "KMou商品请求 UUID",
            FIF.PALETTE,
            "KMou商品请求 UUID",
            parent=self.musicInThisPCGroup,
            isPassword=True
        )
        self.testCard = PrimaryPushSettingCard(
            "测试",
            FIF.TAG,
            "商品请求测试",
            "商品请求测试",
            self.musicInThisPCGroup
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
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.musicInThisPCGroup.addSettingCard(self.goodsTypeCard)
        self.musicInThisPCGroup.addSettingCard(self.uuidCard)
        self.musicInThisPCGroup.addSettingCard(self.testCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        self.testCard.clicked.connect(self.createSuccessInfoBar)

    def createSuccessInfoBar(self):
        InfoBar.success(
            title="成功",
            content=get_goods_info_kmou(cfg.uuid.value) if cfg.goodsType.value else get_goods_info_srap(),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
