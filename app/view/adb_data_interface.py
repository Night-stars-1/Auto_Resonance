"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2025-02-05 18:42:29
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from qfluentwidgets import ScrollArea
from functools import partial

from app.components.button_card import ButtonCardView
from core.adb.adb_port import get_all_port

from app.common.config import cfg
from app.common.style_sheet import StyleSheet
from app.common.worker import Worker
from core.model.config import config
from app.common.config import qconfig

class ADBDataInterface(ScrollArea):
    """ADB端口信息扫描 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.__initWidget()

    def __initWidget(self):
        self.setViewportMargins(0, 20, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("ADBDataInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.loadSamples()

    def showEvent(self, event):
        """当切换到该页面时，触发这个事件"""
        super().showEvent(event) 
        self.basicInputView.removeAllSampleCards()
        self.basicInputView.set_title("加载中...")
        QTimer.singleShot(100, self.start_port_scan)

    def start_port_scan(self):
        """动画结束后调用的方法"""
        self.worker = Worker(get_all_port)
        self.worker.result.connect(self.update_adb)
        self.worker.start()
        
    def loadSamples(self):
        """load samples"""
        self.basicInputView = ButtonCardView("加载中...", parent=self.scrollWidget)

        self.vBoxLayout.addWidget(self.basicInputView)

    def update_adb(self, data: dict[str, str]):
        self.basicInputView.set_title("ADB信息")
        for name, port in data.items():
            self.basicInputView.addSampleCard(
                icon=":/gallery/images/controls/Button.png",
                title=name,
                content=f"127.0.0.1:{port}",
                func=partial(self.set_port, port),
            )

    def set_port(self, port: str):
        qconfig.set(cfg.adbPort, port)
        qconfig.set(cfg.emulatorType, "Custom")
    