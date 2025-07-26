"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-07 23:54:39
LastEditTime: 2024-05-10 23:18:18
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import ConfigItem, FluentIconBase, SettingCard, SpinBox, qconfig

from app.common.signal_bus import signalBus


class SpinBoxSettingCard(SettingCard):
    """Setting card with a push button"""

    def __init__(
        self,
        configItem: ConfigItem,
        icon: Union[str, QIcon, FluentIconBase],
        title: str,
        content=None,
        spin_box_min: int = 0,
        spin_box_max: int = 100,
        parent=None,
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

        self.spinBox = SpinBox(self)
        self.spinBox.setRange(spin_box_min, spin_box_max)
        self.spinBox.setValue(configItem.value)

        self.spinBox.valueChanged.connect(self.valueChanged)
        self.hBoxLayout.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def valueChanged(self, value: int):
        qconfig.set(self.configItem, value)
