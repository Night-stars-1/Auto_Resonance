"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-28 22:46:58
LastEditTime: 2024-05-10 23:18:06
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict, List, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from qfluentwidgets import CheckBox, ConfigItem, FluentIconBase, SettingCard, qconfig


class CheckboxGroup(QWidget):
    """水平复选框群组"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.checkConfigItems: Dict[str, ConfigItem] = {}
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 5, 0)
        self.hBoxLayout.setSpacing(5)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)

    def addCheckbox(self, text: str, configItem: ConfigItem = None, parent=None):
        checkbox = CheckBox(text=text, parent=parent)
        self.hBoxLayout.addWidget(checkbox)

        self.checkConfigItems[text] = configItem
        checkbox.setChecked(configItem.value)
        checkbox.stateChanged.connect(
            lambda: self.onCheckStateChanged(checkbox, configItem)
        )

    def onCheckStateChanged(self, checkbox: CheckBox, configItem: ConfigItem):
        qconfig.set(configItem, checkbox.isChecked())

    def getAllAccept(self):
        return {
            description: configItem.name
            for description, configItem in self.checkConfigItems.items()
            if configItem.value
        }


class CheckboxGroupCard(SettingCard):
    """水平复选框群组"""

    def __init__(
        self, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None
    ):
        super().__init__(icon=icon, title=title, content=content, parent=parent)
        self.checkboxGroup = CheckboxGroup(self)
        self.hBoxLayout.addWidget(self.checkboxGroup, 0, Qt.AlignRight)

    def addCheckbox(self, text: str, configItem: ConfigItem = None, parent=None):
        self.checkboxGroup.addCheckbox(text, configItem, parent)

    def onCheckStateChanged(self, checkbox: CheckBox, configItem: ConfigItem):
        self.checkboxGroup.onCheckStateChanged(checkbox, configItem)

    def getAllAccept(self):
        return self.checkboxGroup.getAllAccept()
