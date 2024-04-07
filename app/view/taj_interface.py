# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from loguru import logger
from qfluentwidgets import ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, SettingCardGroup

from ..common.utils import debounce, read_json, save_json
from ..common.style_sheet import StyleSheet
from ..components.combo_box_title_card import ComboBoxTitleCard

CITYDATA = {
    "7号自由港": {
        "1": ["关卡71", "关卡72", "关卡73", "所有"],
        "2": ["关卡74", "关卡75", "关卡76", "所有"],
        "3": ["关卡77", "关卡78", "关卡79", "所有"],
    },
    "8号自由港": {
        "1": ["关卡71", "关卡72", "关卡73", "所有"],
        "2": ["关卡74", "关卡75", "关卡76", "所有"],
        "3": ["关卡77", "关卡78", "关卡79", "所有"],
    },
    "9号自由港": {
        "1": ["关卡71", "关卡72", "关卡73", "所有"],
        "2": ["关卡74", "关卡75", "关卡76", "所有"],
        "3": ["关卡77", "关卡78", "关卡79", "所有"],
    },
}
SERIAL_NUMBER2POS = {
    "1": [635, 662],
    "2": [890, 663],
    "3": [1150, 663],
}
POS2SERIAL_NUMBER = {
    '[635, 662]': "1",
    '[890, 663]': "2",
    '[1150, 663]': "3"
}
ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG = [
    {
        "type": "wait",
        "image": "railway_safety_bureau/railway_safety_bureau.png",
        "cropped_pos1": [174, 444],
        "cropped_pos2": [294, 547],
        "trynum": 10
    },
    {
        "type": "click",
        "pos": [1137, 660]
    },
    {
        "type": "judgement_text",
        "text": "差异",
        "success": None,
        "fail": [
            {
                "type": "click",
                "pos": [87, 38]
            },
            {
                "type": "wait_time",
                "seconds": 1
            },
            {
                "type": "click",
                "pos": [932, 306]
            }
        ],
        "must_succeed": True
    },
    {
        "type": "click",
        "pos": [883, 540]
    },
    {
        "type": "click_image",
        "image": "railway_safety_bureau/start_attack.png",
        "cropped_pos1": [1133, 128],
        "cropped_pos2": [1263, 628],
        "trynum": 10
    },
    {
        "type": "wait_fight_end"
    },
    {
        "type": "click",
        "pos": [1154, 628]
    },
    {
        "type": "click",
        "pos": [1154, 628]
    }
]
JOIN_RAILWAY_SAFTETY_BUREAU_CONFIG = [
    {
        "type": "click_station",
        "name": "7号自由港"
    },
    {
        "type": "go_outlets",
        "name": "铁安局"
    },
    {
        "type": "wait",
        "image": "railway_safety_bureau/railway_safety_bureau.png",
        "cropped_pos1": [875, 27],
        "cropped_pos2": [1093, 158],
        "trynum": 10
    },
    {
        "type": "click",
        "pos": [1137, 660]
    }
]

class TajInterface(ScrollArea):
    """铁安局 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.join_config = read_json("actions/tasks/join_railway_safety_bureau.json", JOIN_RAILWAY_SAFTETY_BUREAU_CONFIG)
        self.attack_config = read_json("actions/tasks/attack_railway_safety_bureau.json", ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel("铁安局", self)

        # personalization
        self.configGroup = SettingCardGroup("配置", self.scrollWidget)

        self.cityCard = ComboBoxTitleCard(
            FIF.LANGUAGE,
            "城市",
            options=list(CITYDATA.keys()),
            default=self.join_config[0].get('name'),
            content="选择刷取铁安局的城市",
            parent=self.configGroup,
        )
        self.cityCard.comboBox.currentIndexChanged.connect(self.set_level_card)
        self.levelSerialNumber = ComboBoxTitleCard(
            FIF.LANGUAGE,
            "关卡序号",
            options=['1', '2', '3'],
            default=POS2SERIAL_NUMBER.get(str(self.attack_config[1].get("pos", [635, 662]))),
            content="选择刷取铁安局的关卡序号",
            parent=self.configGroup,
        )
        self.levelSerialNumber.comboBox.currentIndexChanged.connect(self.set_level_card)
        self.levelCard = ComboBoxTitleCard(
            FIF.LANGUAGE,
            "关卡名称",
            options=CITYDATA.get(self.cityCard.value, {}).get(self.levelSerialNumber.value, ["所有"]),
            default=self.attack_config[2].get("text"),
            content="选择刷取铁安局的关卡名称",
            parent=self.configGroup,
        )
        self.levelCard.comboBox.currentIndexChanged.connect(self.save_config)
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
        logger.info(level_value)
        ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG[1]["pos"] = SERIAL_NUMBER2POS[serial_number_value]
        if level_value == "所有":
            ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG[2]["is_use"] = False
        else:
            ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG[2]["text"] = level_value
            ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG[2]["is_use"] = True
        JOIN_RAILWAY_SAFTETY_BUREAU_CONFIG[0]['name'] = city_value
        save_json("actions/tasks/attack_railway_safety_bureau.json", ATTACK_RAILWAY_SAFTETY_BUREAU_CONFIG)
        save_json("actions/tasks/join_railway_safety_bureau.json", JOIN_RAILWAY_SAFTETY_BUREAU_CONFIG)
