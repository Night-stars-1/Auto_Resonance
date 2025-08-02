"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:27:03
LastEditTime: 2025-02-11 19:11:04
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
from typing import Union

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget
from loguru import logger
from qfluentwidgets import DotInfoBadge
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    InfoBadgePosition,
    InfoBar,
    InfoBarPosition,
    MSFluentWindow,
    NavigationItemPosition,
    SplashScreen,
    FluentIconBase,
    SystemThemeListener,
    isDarkTheme,
    setTheme,
    MessageBox
)

import app.common.resource  # 图标数据
from app.common.config import VERSION, cfg, isWin11
from app.common.signal_bus import signalBus
from app.components.update_message_box import UpdateMessageBox
from app.utils.constants import ICON_PATH, ROOT_PATH
from app.utils.utils import is_chinese
from app.view.two_city_run_business_interface import TwoRunBusinessInterface
from core.utils.update.base_update_utils import UpdateStatus
from core.utils.update.mirror_update_utils import MirrorUpdateUtils

from .adb_data_interface import ADBDataInterface
from .home_interface import HomeInterface
from .logger_interface import LoggerInterface
from .setting_interface import SettingInterface


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.wights = {}

        # 主题监听器
        self.themeListener = SystemThemeListener(self)

        self.initWindow()
        self.setInterface()

        self.initNavigation()

        self.connectSignalToSlot()

        self.splashScreen.finish()
        # 检查更新
        self.updater = MirrorUpdateUtils()
        # self.checkUpdate()
        # 启用主题监听器
        self.themeListener.start()
        
        self.checkChinesePath()

    def connectSignalToSlot(self):
        signalBus.switchToCard.connect(self.switchToCard)
        # 监听主题切换
        cfg.themeChanged.connect(setTheme)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.two_run_business_interface, FIF.TRAIN, "端点跑商")
        self.addSubInterface(self.adb_data_interface, FIF.GAME, "ADB信息")

        # 底部按钮
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
            onClick=self._update,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "设置",
            position=NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(str(ICON_PATH / "logo.ico")))
        self.setWindowTitle(f"黑月无人驾驶 - {VERSION}")

        self.setMicaEffectEnabled(isWin11())
        self.setResizeEnabled(False)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = self.screen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def setInterface(self):
        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.loggerInterface = LoggerInterface(self)
        self.settingInterface = SettingInterface(self)
        self.two_run_business_interface = TwoRunBusinessInterface(self)
        self.adb_data_interface = ADBDataInterface(self)

        self.update_message_box = UpdateMessageBox(self)

    def addSubInterface(
        self,
        interface: QWidget,
        icon: Union[FluentIconBase, QIcon, str],
        text: str,
        selectedIcon=None,
        position=NavigationItemPosition.TOP,
        isTransparent=False,
    ):
        super().addSubInterface(
            interface, icon, text, selectedIcon, position, isTransparent
        )
        self.wights[interface.objectName()] = interface

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.splashScreen.resize(self.size())

    def switchToCard(self, routeKey):
        """切换到指定界面"""
        self.switchTo(self.wights[routeKey])

    def closeEvent(self, e):
        # 停止监听器线程
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # 云母特效启用时需要增加重试机制
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

    def _update(self):
        """
        检查更新
        """
        update_status = self.updater.get_update_status(cfg.mirrorCdk.value, reload=True)
        if update_status == UpdateStatus.UPDATE:
            self.update_message_box.show(cfg.mirrorCdk.value)
        elif update_status == UpdateStatus.FAILED:
            InfoBar.error(
                title="检查更新失败",
                content="请稍后重试",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        elif update_status == UpdateStatus.NOSUPPORT:
            InfoBar.error(
                title="更新程序只支持打包成exe后运行",
                content="",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        elif update_status == UpdateStatus.LATEST:
            InfoBar.success(
                title="当前已是最新版本",
                content="",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        elif update_status == UpdateStatus.FAILDCDK:
            InfoBar.error(
                title="Mirror CDK校验失败",
                content="请检查Mirror CDK是否正确",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
        else:
            InfoBar.error(
                title="检查更新失败",
                content="请稍后重试",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )

    def checkUpdate(self):
        update_status = self.updater.get_update_status(cfg.mirrorCdk.value)
        if update_status == UpdateStatus.UPDATE and self.updateButton is not None:
            self.updateBadge = DotInfoBadge.error(
                parent=self.navigationInterface,
                target=self.updateButton,
                position=InfoBadgePosition.NAVIGATION_ITEM,
            )
            self.updateBadge.setFixedSize(10, 10)

    def checkChinesePath(self):
        if is_chinese(str(ROOT_PATH)):
            w = MessageBox("兼容性警告", "程序运行在中文路径上，请移动至英文路径", self)
            
            w.yesButton.setText("知道了")
            w.cancelButton.hide()
            w.buttonLayout.insertStretch(1)
            w.exec()
