# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QButtonGroup,
    QVBoxLayout,
    QHBoxLayout,
)

from qfluentwidgets import LineEdit, ExpandGroupSettingCard, RadioButton, ConfigItem
from app.common.config import qconfig
from app.common.icon import FluentIconBase


class CustomAdbSettingCard(ExpandGroupSettingCard):
    """Custom adb setting card"""

    def __init__(
        self,
        configItem: ConfigItem,
        customConfigItem: ConfigItem,
        icon: Union[str, QIcon, FluentIconBase],
        title: str,
        content=None,
        texts: dict = {},
        parent=None,
    ):
        super().__init__(icon, title, content, parent=parent)
        self.texts = texts
        self.configItem = configItem
        self.customConfigItem = customConfigItem
        self.defaultItem = "Custom"
        self.customItem = qconfig.get(configItem)

        self.choiceLabel = QLabel(self)
        self.radioWidget = QWidget(self.view)
        self.radioLayout = QVBoxLayout(self.radioWidget)
        self.defaultRadioButton = RadioButton(
            "自定义ADB端口", self.radioWidget
        )
        self.defaultRadioButton.setProperty("option", self.defaultItem)
        self.defaultRadioButton.setChecked(True) # self.configItem.value == self.defaultItem
        # self.customRadioButton = RadioButton(self.tr("Custom color"), self.radioWidget)
        self.buttonGroup = QButtonGroup(self)
        for text, option in texts.items():
            button = RadioButton(text, self.view)
            self.buttonGroup.addButton(button)
            self.radioLayout.addWidget(button)
            button.setProperty("option", option)
            button.setChecked(option == self.configItem.value)

        self.customItemWidget = QWidget(self.view)
        self.customItemLayout = QHBoxLayout(self.customItemWidget)
        self.customLabel = QLabel("自定义ADB端口", self.customItemWidget)
        self.chooseItemLineEdit = LineEdit(self.customItemWidget)
        self.chooseItemLineEdit.setText(self.customConfigItem.value)

        self.__initLayout()

    def __initLayout(self):
        self.addWidget(self.choiceLabel)

        self.radioLayout.setSpacing(19)
        self.radioLayout.setAlignment(Qt.AlignTop)
        self.radioLayout.setContentsMargins(48, 18, 0, 18)
        self.buttonGroup.addButton(self.defaultRadioButton)
        self.radioLayout.addWidget(self.defaultRadioButton)
        
        self.radioLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.customItemLayout.setContentsMargins(48, 18, 44, 18)
        self.customItemLayout.addWidget(self.customLabel, 0, Qt.AlignLeft)
        self.customItemLayout.addWidget(self.chooseItemLineEdit, 0, Qt.AlignRight)
        self.customItemLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.addGroupWidget(self.radioWidget)
        self.addGroupWidget(self.customItemWidget)

        self.__initWidget()

    def __initWidget(self):
        if self.defaultItem == self.customItem:
            self.chooseItemLineEdit.setEnabled(True)
        else:
            self.chooseItemLineEdit.setEnabled(False)

        self.choiceLabel.setText(self.buttonGroup.checkedButton().text())
        self.choiceLabel.adjustSize()

        self.chooseItemLineEdit.setObjectName("chooseColorButton")

        self.buttonGroup.buttonClicked.connect(self.__onRadioButtonClicked)
        self.chooseItemLineEdit.textChanged.connect(self.__onChooseItemTextChanged)

    def __onRadioButtonClicked(self, button: RadioButton):
        """radio button clicked slot"""
        if button.text() == self.choiceLabel.text():
            return

        self.choiceLabel.setText(button.text())
        self.choiceLabel.adjustSize()
        if button is not self.defaultRadioButton:
            self.chooseItemLineEdit.setDisabled(True)
        else:
            self.chooseItemLineEdit.setDisabled(False)
        option = button.property("option")
        qconfig.set(self.configItem, option)

    def __onChooseItemTextChanged(self, text):
        qconfig.set(self.customConfigItem, text)
