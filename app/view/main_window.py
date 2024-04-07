"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:27:03
LastEditTime: 2024-04-07 13:00:04
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

# coding: utf-8
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    FluentWindow,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    MSFluentWindow,
    NavigationAvatarWidget,
    NavigationBarPushButton,
    NavigationItemPosition,
    SplashScreen,
    Theme,
    setTheme,
    setThemeColor,
    toggleTheme,
)

from ..common import resource
from ..common.config import cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from .home_interface import HomeInterface
from .logger_interface import LoggerInterface
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

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToCard.connect(self.switchToCard)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, "Home")
        self.wights[self.homeInterface.objectName()] = self.homeInterface
        self.addSubInterface(self.tajInterface, FIF.AIRPLANE, "铁安局")
        self.wights[self.tajInterface.objectName()] = self.tajInterface
        self.addSubInterface(self.loggerInterface, FIF.ALIGNMENT, "日志")
        self.wights[self.loggerInterface.objectName()] = self.loggerInterface

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon("./app/resource/images/logo.png"))
        self.setWindowTitle("黑月无人驾驶")

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
