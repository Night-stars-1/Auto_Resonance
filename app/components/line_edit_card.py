"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-07 23:54:39
LastEditTime: 2024-04-10 01:11:23
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Optional, Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from qfluentwidgets import (
    SettingCard,
    FluentIconBase,
    LineEdit,
    PasswordLineEdit,
    ConfigItem,
)


class LineEditCard(SettingCard):
    """card with a push button"""

    text_change = pyqtSignal()

    def __init__(
        self,
        icon: Union[str, QIcon, FluentIconBase],
        holderText: str,
        title: str,
        default: str = "",
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

        if isPassword:
            self.lineEdit = PasswordLineEdit(self)
        else:
            self.lineEdit = LineEdit(self)
        self.lineEdit.setText(default)
        self.lineEdit.setPlaceholderText(holderText)

        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
