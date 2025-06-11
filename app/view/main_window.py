"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:27:03
LastEditTime: 2025-02-11 19:11:04
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import asyncio
from typing import Union

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from loguru import logger
from qfluentwidgets import DotInfoBadge
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    InfoBadgePosition,
    InfoBar,
    InfoBarPosition,
    MSFluentWindow,
    NavigationBarPushButton,
    NavigationItemPosition,
    SplashScreen,
)

from app.common import resource  # 图标数据
from app.common.config import VERSION, cfg
from app.common.icon import FluentIconBase
from app.common.signal_bus import signalBus
from app.components.update_message_box import UpdateMessageBox
from app.view.daily_task_interface import DailyTaskInterface
from app.view.two_city_run_business_interface import TwoRunBusinessInterface
from core.utils.update.base_update_utils import UpdateStatus
from core.utils.update.mirror_update_utils import MirrorUpdateUtils

from .adb_data_interface import ADBDataInterface
from .home_interface import HomeInterface
from .logger_interface import LoggerInterface
from .setting_interface import SettingInterface
from .taj_interface import TajInterface


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.wights = {}

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.tajInterface = TajInterface(self)
        self.loggerInterface = LoggerInterface(self)
        self.settingInterface = SettingInterface(self)
        self.daily_task_interface = DailyTaskInterface(self)
        self.two_run_business_interface = TwoRunBusinessInterface(self)
        self.adb_data_interface = ADBDataInterface(self)

        self.update_message_box = UpdateMessageBox(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()
        # 检查更新
        self.updater = MirrorUpdateUtils()
        self.checkUpdate()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToCard.connect(self.switchToCard)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.tajInterface, FIF.AIRPLANE, "铁安局")
        self.addSubInterface(self.daily_task_interface, FIF.CALENDAR, "每日任务")
        self.addSubInterface(self.two_run_business_interface, FIF.TRAIN, "端点跑商")
        self.addSubInterface(self.adb_data_interface, FIF.GAME, "ADB信息")

        # add custom widget to bottom
        self.addSubInterface(
            self.loggerInterface,
            FIF.ALIGNMENT,
            "日志",
            position=NavigationItemPosition.BOTTOM,
        )
        self.updateButton = self.navigationInterface.addItem(
            routeKey="Update",
            icon=FIF.UPDATE,
            text="更新",
            onClick=self.Update,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM,
        )

    def addSubInterface(
        self,
        interface: QWidget,
        icon: Union[FluentIconBase, QIcon, str],
        text: str,
        selectedIcon=None,
        position=NavigationItemPosition.TOP,
        isTransparent=False,
    ) -> NavigationBarPushButton:
        super().addSubInterface(
            interface, icon, text, selectedIcon, position, isTransparent
        )
        self.wights[interface.objectName()] = interface

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon("./app/resource/images/logo.ico"))
        self.setWindowTitle(f"黑月无人驾驶 - {VERSION}")

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        self.setResizeEnabled(False)
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splashScreen.resize(self.size())

    def switchToCard(self, routeKey):
        """switch to card"""
        self.switchTo(self.wights[routeKey])

    def Update(self):
        """
        说明:
            检查更新
        """
        update_status = self.updater.get_update_status(cfg.mirrorCdk.value, reload=True)
        if update_status == UpdateStatus.UPDATE:
            self.update_message_box.show(cfg.mirrorCdk.value)
        elif update_status == UpdateStatus.FAILED:
            InfoBar.error(
                title="检查更新失败",
                content="请稍后重试",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        elif update_status == UpdateStatus.NOSUPPORT:
            InfoBar.error(
                title="更新程序只支持打包成exe后运行",
                content="",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        elif update_status == UpdateStatus.LATEST:
            InfoBar.success(
                title="当前已是最新版本",
                content="",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        elif update_status == UpdateStatus.FAILDCDK:
            InfoBar.error(
                title="Mirror CDK校验失败",
                content="请检查Mirror CDK是否正确",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        else:
            InfoBar.error(
                title="检查更新失败",
                content="请稍后重试",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )

    def checkUpdate(self):
        update_status = self.updater.get_update_status(cfg.mirrorCdk.value)
        if update_status == UpdateStatus.UPDATE:
            self.updateBadge = DotInfoBadge.error(
                parent=self.navigationInterface,
                target=self.updateButton,
                position=InfoBadgePosition.NAVIGATION_ITEM,
            )
            self.updateBadge.setFixedSize(10, 10)
