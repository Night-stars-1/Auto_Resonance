"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 19:53:49
LastEditTime: 2024-04-07 13:24:45
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from typing import Any, Dict, List, Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import ComboBox
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import FluentIconBase, SettingCard, setFont, setTheme, setThemeColor


class ComboBoxTitleCard(SettingCard):
    """带有组合框的标题卡"""

    def __init__(
        self,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        options: Union[List[str], Dict[str, Any]],
        default: Optional[str] = None,
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.comboBox = ComboBox(self)

        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        if isinstance(options, list):
            self.value = options[0] if len(options) > 0 else None
            if default not in options:
                default = None
            for option in options:
                self.comboBox.addItem(option, userData=option)
        elif isinstance(options, dict):
            self.value = list(options.keys())[0] if len(options) > 0 else None
            if default not in list(options.values()):
                default = None
            for option, value in options.items():
                self.comboBox.addItem(option, userData=value)
                self.comboBox.setCurrentText(option)

        self.value = default or self.value
        self.comboBox.setCurrentText(self.value)
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)

    def _onCurrentIndexChanged(self, index: int):
        self.value = self.comboBox.itemData(index)


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = ComboBoxTitleCard(
        FIF.ALIGNMENT,
        "标题",
        options=["选项1", "选项2", "选项3"],
    )
    w.show()
    app.exec_()
