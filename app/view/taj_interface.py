"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 19:32:25
LastEditTime: 2024-04-14 16:02:34
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, SettingCardGroup

from core.models.config import config

from ..common.style_sheet import StyleSheet
from ..common.utils import debounce
from ..components.combo_box_title_card import ComboBoxTitleCard
from ..components.line_edit_card import LineEditCard
from ..components.tab_widget import TabWidget

CITYDATA = {
    "修格里城": {
        "1": ["所有", "横行霸道", "除恶务本"],
        "2": ["所有", "蔓草难除", "症结"],
        "3": ["所有", "适可而止"],
    },
    "7号自由港": {
        "1": ["所有", "横冲直撞"],
        "2": ["所有", "危险 区", "鸟覆危巢"],
        "3": ["所有", "迷途", "差异"],
    },
    "曼德矿场": {
        "1": ["所有", "谜题", "核心"],
        "2": ["所有", "巢穴", "误工"],
        "3": ["所有", "迷失", "嘎！！！"],
    },
    "澄明数据中心": {
        "1": ["所有", "细节调查", "旧时代遗患"],
        "2": ["所有", "不祥预感", "危险应验"],
        "3": ["所有", "妨碍汇合", "一网打尽"],
    },
}
SERIAL_NUMBER2POS = {
    "1": [635, 662],
    "2": [890, 663],
    "3": [1150, 663],
}
POS2SERIAL_NUMBER = {"[635, 662]": "1", "[890, 663]": "2", "[1150, 663]": "3"}


class TajConfigInterface(ScrollArea):
    """铁安局 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.settingLabel = QLabel("铁安局", self)

        # personalization
        self.configGroup = SettingCardGroup("配置", self.scrollWidget)

        self.cityCard = ComboBoxTitleCard(
            FIF.LANGUAGE,
            "城市",
            options=list(CITYDATA.keys()),
            default=config.rsb.city,
            content="选择刷取铁安局的城市",
            parent=self.configGroup,
        )
        self.cityCard.comboBox.currentIndexChanged.connect(self.set_level_card)
        self.levelSerialNumber = ComboBoxTitleCard(
            FIF.LANGUAGE,
            "关卡序号",
            options=["1", "2", "3"],
            default=POS2SERIAL_NUMBER.get(str(config.rsb.levelSerialPos)),
            content="选择刷取铁安局的关卡序号",
            parent=self.configGroup,
        )
        self.levelSerialNumber.comboBox.currentIndexChanged.connect(self.set_level_card)
        self.levelCard = ComboBoxTitleCard(
            FIF.LANGUAGE,
            "关卡名称",
            options=CITYDATA.get(self.cityCard.value, {}).get(
                self.levelSerialNumber.value, ["所有"]
            ),
            default=config.rsb.name,
            content="选择刷取铁安局的关卡名称",
            parent=self.configGroup,
        )
        self.levelCard.comboBox.currentIndexChanged.connect(self.save_config)

        self.numCard = LineEditCard(
            FIF.LANGUAGE,
            "刷取次数",
            "刷取次数",
            default=str(config.rsb.num),
            content="选择刷取铁安局的关卡名称",
            parent=self.configGroup,
        )
        self.numCard.lineEdit.textChanged.connect(self.save_config)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("TajInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.__initLayout()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.configGroup.addSettingCard(self.cityCard)
        self.configGroup.addSettingCard(self.levelSerialNumber)
        self.configGroup.addSettingCard(self.levelCard)
        self.configGroup.addSettingCard(self.numCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.configGroup)

    def set_level_card(self, index: int):
        """
        说明:
            设置关卡卡片的选项
        参数:
            :param index: 选项索引
        """
        city_value = self.cityCard.value
        serial_number_value = self.levelSerialNumber.value
        level_data = CITYDATA.get(city_value, {}).get(serial_number_value, ["所有"])

        self.levelCard.comboBox.clear()
        for value in level_data:
            self.levelCard.comboBox.addItem(value, userData=value)

    @debounce(0.1)
    def save_config(self, index: int):
        """
        说明:
            保存配置
        参数:
            :param index: 选项索引
        """
        city_value = self.cityCard.value
        serial_number_value = self.levelSerialNumber.value
        level_value = self.levelCard.value
        config.rsb.city = city_value
        config.rsb.levelSerialPos = SERIAL_NUMBER2POS[serial_number_value]
        config.rsb.name = level_value
        config.rsb.num = int(self.numCard.lineEdit.text())
        config.save_config()


class TajInterface(TabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TajInterface")

        self.tajConfigInterface = TajConfigInterface(self)

        self.__initWidget()

    def __initWidget(self):
        self.addSubInterface(
            self.tajConfigInterface, "TajConfigInterface", "铁安局配置1", FIF.LANGUAGE
        )
