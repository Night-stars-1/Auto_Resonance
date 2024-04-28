"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 22:03:56
LastEditTime: 2024-04-28 23:05:29
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLayout, QVBoxLayout, QWidget
from qfluentwidgets import CardWidget, FlowLayout, IconWidget, TextWrap

from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet


class SampleCard(CardWidget):
    """Sample card"""

    def __init__(self, icon, title, content, func, routekey, index, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.func = func
        self.routekey = routekey

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(360, 90)
        self.iconWidget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if self.routekey:
            signalBus.switchToCard.emit(self.routekey)
        self.func()


class ButtonCardView(QWidget):
    """Sample card view"""

    def __init__(self, title: str, header: QWidget = None, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(header)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName("viewTitleLabel")
        StyleSheet.SAMPLE_CARD.apply(self)

    def addSampleCard(self, icon, title, content, func, routekey=None):
        """add sample card"""
        card = SampleCard(icon, title, content, func, routekey, self)
        self.flowLayout.addWidget(card)
        return card
