"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-07 23:54:39
LastEditTime: 2024-05-10 23:06:09
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from qfluentwidgets import (
    SettingCard,
    FluentIconBase,
    LineEdit,
    PasswordLineEdit,
    ConfigItem,
    qconfig
)

class LineEditSettingCard(SettingCard):
    """Setting card with a push button"""

    text_change = pyqtSignal()

    def __init__(
        self,
        configItem: ConfigItem,
        holderText: str,
        icon: Union[str, QIcon, FluentIconBase],
        title: str,
        content=None,
        parent=None,
        isPassword=False,
    ):
        """
        Parameters
        ----------
        text: str
            the text of push button

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.configItem = configItem

        if isPassword:
            self.lineEdit = PasswordLineEdit(self)
        else:
            self.lineEdit = LineEdit(self)
        self.lineEdit.setText(qconfig.get(self.configItem))
        self.lineEdit.setPlaceholderText(holderText)

        self.lineEdit.textChanged.connect(self.textChanged)
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        # self.button.clicked.connect(self.clicked)

    def textChanged(self, text):
        qconfig.set(self.configItem, text)
