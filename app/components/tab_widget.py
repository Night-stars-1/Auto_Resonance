"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-14 15:58:27
LastEditTime: 2024-04-14 15:59:47
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TabBar

from ..common.style_sheet import StyleSheet


class TabWidget(QWidget):
    """铁安局 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabBar = TabBar(self)
        self.tabView = QWidget(self)
        self.stackedWidget = QStackedWidget(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)

        self.initWidget()

    def initWidget(self):
        self.initLayout()

        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        self.hBoxLayout.addWidget(self.tabView, 1)
        # self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget, 1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.setFixedHeight(580)

    def addSubInterface(self, widget: QWidget, objectName, text, icon):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )
