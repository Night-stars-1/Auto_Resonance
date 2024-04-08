from typing import Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from qfluentwidgets import SettingCard, FluentIconBase, LineEdit
from qfluentwidgets import OptionsConfigItem, qconfig

class LineEditSettingCard(SettingCard):
    """ Setting card with a push button """

    text_change = pyqtSignal()

    def __init__(self, configItem: str, holderText: str, icon: Union[str, QIcon, FluentIconBase], title: str, content=None, parent=None):
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

        self.lineEdit = LineEdit(self)
        self.lineEdit.setText(qconfig.get(self.configItem))
        self.lineEdit.setPlaceholderText(holderText)
        self.lineEdit.textChanged.connect(self.textChanged)
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        #self.button.clicked.connect(self.clicked)
    
    def textChanged(self, text):
        qconfig.set(self.configItem, text)
