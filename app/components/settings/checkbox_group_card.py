"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-28 22:46:58
LastEditTime: 2024-12-28 01:23:41
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict, List, Optional

from PySide6.QtWidgets import QWidget
from qfluentwidgets import CheckBox, ConfigItem, qconfig

from app.components.layout.flow_layout import FlowLayout


class CheckboxGroup(QWidget):
    """水平复选框群组"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.checkConfigItems: Dict[str, ConfigItem] = {}
        self.checkboxGroup: List[CheckBox] = []
        self.flowLayout = FlowLayout(self)
        self.flowLayout.setSpacing(5)  # 控件间距
        # 更新自身高度
        self.flowLayout.layoutChanged.connect(self.updateFlowLayoutHeight)

    def updateFlowLayoutHeight(self):
        """更新 FlowLayout 高度"""
        self.setFixedHeight(self.flowLayout.sizeHint().height())

    def addCheckbox(self, text: str, configItem: Optional[ConfigItem] = None, parent=None):
        checkbox = CheckBox(text=text, parent=parent)
        self.checkboxGroup.append(checkbox)
        self.flowLayout.addWidget(checkbox)

        if configItem:
            self.checkConfigItems[text] = configItem
            checkbox.setChecked(configItem.value)
            checkbox.stateChanged.connect(
                lambda: self.onCheckStateChanged(checkbox, configItem)
            )
        else:
            checkbox.setChecked(False)
        return checkbox

    def onCheckStateChanged(self, checkbox: CheckBox, configItem: ConfigItem):
        qconfig.set(configItem, checkbox.isChecked())

    def count(self):
        return sum(1 for checkbox in self.checkboxGroup if checkbox.isChecked())

    def getAllAccept(self):
        return {
            description: configItem.name
            for description, configItem in self.checkConfigItems.items()
            if configItem.value
        }

