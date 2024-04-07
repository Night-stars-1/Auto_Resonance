"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:52:14
LastEditTime: 2024-04-07 13:42:53
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import PlainTextEdit, ScrollArea, isDarkTheme

from ..common.style_sheet import StyleSheet
import core.logger


class LoguruHandler:
    def __init__(self, widget: PlainTextEdit):
        self.widget = widget
        self.widget.setReadOnly(True)

    def write(self, message):
        self.widget.appendPlainText(message[:-1])

    def flush(self): ...


class LoggerInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.log_widget = PlainTextEdit(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()
        self.loadLogger()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("LoggerInterface")
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.log_widget)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadLogger(self):
        logger.add(
            LoguruHandler(self.log_widget),
            level="INFO",
            format="{message}",
        )
