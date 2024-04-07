"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:52:14
LastEditTime: 2024-04-07 16:21:05
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import PlainTextEdit, ScrollArea, isDarkTheme

from core.logger import logger

from ..common.style_sheet import StyleSheet


class LoguruHandler(QObject):
    # 创建一个信号
    new_log_signal = pyqtSignal(str)

    def __init__(self, widget: PlainTextEdit):
        super().__init__()
        self.widget = widget
        self.widget.setReadOnly(True)
        # 连接信号到槽，安全地更新文本控件
        self.new_log_signal.connect(self.widget.appendPlainText)

    def write(self, message):
        # 使用信号发送消息
        self.new_log_signal.emit(message[:-1])


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
            enqueue=True,
            format="{message}",
        )
