# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QButtonGroup,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)

from qfluentwidgets import ColorDialog, ExpandGroupSettingCard, RadioButton, ConfigItem
from app.common.config import qconfig
from app.common.icon import FluentIconBase


class CustomAdbSettingCard(ExpandGroupSettingCard):
    """Custom adb setting card"""

    def __init__(
        self,
        configItem: ConfigItem,
        icon: Union[str, QIcon, FluentIconBase],
        title: str,
        content=None,
        texts=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent=parent)
        self.configItem = configItem
        self.defaultItem = configItem.defaultValue
        self.customItem = qconfig.get(configItem)

        self.choiceLabel = QLabel(self)
        self.radioWidget = QWidget(self.view)
        self.radioLayout = QVBoxLayout(self.radioWidget)
        self.defaultRadioButton = RadioButton(
            self.tr("Default color"), self.radioWidget
        )
        # self.customRadioButton = RadioButton(self.tr("Custom color"), self.radioWidget)
        self.buttonGroup = QButtonGroup(self)
        # for text, option in zip(texts, configItem.options):
        #     button = RadioButton(text, self.view)
        #     self.buttonGroup.addButton(button)
        #     self.radioLayout.addWidget(button)
            # button.setProperty(self.configName, option)

        self.customItemWidget = QWidget(self.view)
        self.customItemLayout = QHBoxLayout(self.customItemWidget)
        self.customLabel = QLabel(self.tr("Custom color"), self.customItemWidget)
        self.chooseItemButton = QPushButton(
            self.tr("Choose color"), self.customItemWidget
        )

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()

        if self.defaultItem != self.customItem:
            self.customRadioButton.setChecked(True)
            self.chooseItemButton.setEnabled(True)
        else:
            self.defaultRadioButton.setChecked(True)
            self.chooseItemButton.setEnabled(False)

        self.choiceLabel.setText(self.buttonGroup.checkedButton().text())
        self.choiceLabel.adjustSize()

        self.chooseItemButton.setObjectName("chooseColorButton")

        self.buttonGroup.buttonClicked.connect(self.__onRadioButtonClicked)
        # self.chooseItemButton.clicked.connect(self.__showColorDialog)

    def __initLayout(self):
        self.addWidget(self.choiceLabel)

        self.radioLayout.setSpacing(19)
        self.radioLayout.setAlignment(Qt.AlignTop)
        self.radioLayout.setContentsMargins(48, 18, 0, 18)
        # self.buttonGroup.addButton(self.customRadioButton)
        self.buttonGroup.addButton(self.defaultRadioButton)
        # self.radioLayout.addWidget(self.customRadioButton)
        self.radioLayout.addWidget(self.defaultRadioButton)
        self.radioLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.customItemLayout.setContentsMargins(48, 18, 44, 18)
        self.customItemLayout.addWidget(self.customLabel, 0, Qt.AlignLeft)
        self.customItemLayout.addWidget(self.chooseItemButton, 0, Qt.AlignRight)
        self.customItemLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.addGroupWidget(self.radioWidget)
        self.addGroupWidget(self.customItemWidget)

    def __onRadioButtonClicked(self, button: RadioButton):
        """radio button clicked slot"""
        if button.text() == self.choiceLabel.text():
            return

        self.choiceLabel.setText(button.text())
        self.choiceLabel.adjustSize()

        if button is self.defaultRadioButton:
            self.chooseItemButton.setDisabled(True)
            qconfig.set(self.configItem, self.defaultItem)
        else:
            self.chooseItemButton.setDisabled(False)
            qconfig.set(self.configItem, self.customItem)

    def __onCustomColorChanged(self, color):
        """custom color changed slot"""
        qconfig.set(self.configItem, color)
        self.customItem = QColor(color)
