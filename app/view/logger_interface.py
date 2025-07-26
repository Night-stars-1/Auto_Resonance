"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:52:14
LastEditTime: 2024-04-14 14:20:47
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import PlainTextEdit, ScrollArea

from core.logger import logger

from ..common.style_sheet import StyleSheet


class LoguruHandler(QObject):
    new_log_signal = Signal(str)

    def __init__(self, widget: PlainTextEdit):
        super().__init__()
        self.widget = widget
        self.widget.setReadOnly(True)
        
        self.new_log_signal.connect(self.widget.appendPlainText)

    def write(self, message):
        self.new_log_signal.emit(message[:-1])


class LoggerInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.loggerLabel = QLabel("日志", self)
        self.log_widget = PlainTextEdit(self)

        self.initWidget()
        self.initLayout()
        self.loadLogger()

    def initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("LoggerInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.loggerLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)


    def initLayout(self):
        self.loggerLabel.move(36, 30)

        self.vBoxLayout.setContentsMargins(36, 80, 36, 10)
        self.vBoxLayout.setSpacing(28)
        self.vBoxLayout.addWidget(self.log_widget)

    def loadLogger(self):
        logger.add(
            LoguruHandler(self.log_widget),
            level="INFO",
            format="{message}",
        )
