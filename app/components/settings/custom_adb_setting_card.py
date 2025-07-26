from typing import Optional, Union
from PySide6.QtGui import QIcon

from qfluentwidgets import ConfigItem, FluentIconBase
from app.common.config import qconfig
from app.components.settings.line_edit_setting_card import LineEditSettingCard

from core.control.adb_port import EmulatorInfo, EmulatorType


class CustomAdbSettingCard(LineEditSettingCard):
    """Custom adb setting card"""

    def __init__(
        self,
        configItem: ConfigItem,
        icon: Union[FluentIconBase, str, QIcon],
        title: str,
        content: Optional[str]=None,
        parent=None,
    ):
        self.configItem = configItem
        self.customInfo = EmulatorInfo(name="自定义端口", port=16384, path="", type=EmulatorType.CUSTOM, index=0)
        
        super().__init__(configItem, title, icon, title, content, parent=parent)

    def initText(self):
        info: EmulatorInfo = self.configItem.value
        self.lineEdit.setText(str(info.port))

    def textChanged(self, text: str):
        self.customInfo.port = int(text) if text.isdigit() else 16384
        qconfig.set(self.configItem, self.customInfo)

    def update(self):
        self.initText()
