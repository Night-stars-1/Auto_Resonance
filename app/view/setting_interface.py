"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-07 23:14:47
LastEditTime: 2025-02-11 19:20:13
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QLabel, QWidget
from qfluentwidgets import ExpandLayout, PrimaryPushSettingCard
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, SettingCardGroup, SwitchSettingCard

from app.common.config import cfg
from app.common.style_sheet import StyleSheet
from app.components.settings.custom_adb_setting_card import CustomAdbSettingCard
from app.components.settings.line_edit_setting_card import LineEditSettingCard
from core.model.config import config
from core.model.emulator import emulator_list

MIRROR_URL = "https://mirrorchyan.com/zh/projects?rid=Auto_Resonance&source=auto-resonance-release"


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
        self.mirrorCdkCard = LineEditSettingCard(
            cfg.mirrorCdk,
            "Mirror酱 CDK",
            FIF.LABEL,
            "Mirror酱 CDK",
            parent=self.musicInThisPCGroup,
            isPassword=True,
        )
        self.mirrorCard = PrimaryPushSettingCard(
            "Mirror酱",
            FIF.SHARE,
            "浏览 Mirror 酱",
            "在 Mirror 酱官网购买 CDK",
            self.musicInThisPCGroup,
        )
        # self.goodsTypeCard = SwitchSettingCard(
        #     FIF.TAG,
        #     "数据源",
        #     "开为 KMou，关为 SRAP",
        #     configItem=cfg.goodsType,
        #     parent=self.musicInThisPCGroup,
        # )
        # self.uuidCard = LineEditSettingCard(
        #     cfg.uuid,
        #     "KMou商品请求 UUID",
        #     FIF.LABEL,
        #     "KMou商品请求 UUID",
        #     parent=self.musicInThisPCGroup,
        #     isPassword=True,
        # )
        # self.adbPathCard = LineEditSettingCard(
        #     cfg.adbPath,
        #     "ADB路径",
        #     FIF.PALETTE,
        #     "ADB程序路径",
        #     parent=self.musicInThisPCGroup,
        # )
        self.adbOrderCard = CustomAdbSettingCard(
            cfg.device,
            FIF.GAME,
            "ADB地址",
            "修改该内容自动变为自定义ADB端口",
            parent=self.musicInThisPCGroup,
        )
        # self.adbOrderCard = LineEditSettingCard(
        #     cfg.adbOrder,
        #     "ADB地址",
        #     FIF.PALETTE,
        #     "ADB地址",
        #     parent=self.musicInThisPCGroup,
        # )
        self.isSpeedCard = SwitchSettingCard(
            FIF.MARKET,
            "是否自动加速",
            "是否自动使用加速弹丸",
            parent=self.musicInThisPCGroup,
        )
        self.isAutoPickCard = SwitchSettingCard(
            FIF.TILES,
            "是否自动拾取",
            "是否自动拾取掉落物",
            parent=self.musicInThisPCGroup,
        )
        self.isSpeedCard.setValue(config.global_config.is_speed)
        self.isSpeedCard.switchButton.checkedChanged.connect(self.__onCheckedChanged)
        self.isAutoPickCard.setValue(config.global_config.is_auto_pick)
        self.isAutoPickCard.switchButton.checkedChanged.connect(self.__onCheckedChanged)

        self.mirrorCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(MIRROR_URL))
        )
        self.__initWidget()

    def __onCheckedChanged(self):
        config.global_config.is_speed = self.isSpeedCard.isChecked()
        config.global_config.is_auto_pick = self.isAutoPickCard.isChecked()
        config.save_config()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        # self.musicInThisPCGroup.addSettingCard(self.goodsTypeCard)
        # self.musicInThisPCGroup.addSettingCard(self.uuidCard)
        # self.musicInThisPCGroup.addSettingCard(self.adbPathCard)
        self.musicInThisPCGroup.addSettingCard(self.mirrorCdkCard)
        self.musicInThisPCGroup.addSettingCard(self.mirrorCard)
        self.musicInThisPCGroup.addSettingCard(self.adbOrderCard)
        self.musicInThisPCGroup.addSettingCard(self.isSpeedCard)
        self.musicInThisPCGroup.addSettingCard(self.isAutoPickCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)

    def showEvent(self, event):
        """当切换到该页面时，触发这个事件"""
        super().showEvent(event)
        # 刷新adb设置
        self.adbOrderCard.update()
