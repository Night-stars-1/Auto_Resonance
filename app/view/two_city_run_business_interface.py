"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2025-02-10 23:25:35
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from functools import partial
from typing import Dict

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import CheckBox, ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea

from app.common.config import cfg
from app.common.running_business_config import CITYS
from app.common.signal_bus import signalBus
from app.common.style_sheet import StyleSheet
from app.common.worker import Worker
from app.components.primary_push_load_card import PrimaryPushLoadCard
from app.components.settings.checkbox_group_card import CheckboxGroup
from app.components.settings.spin_box_setting_card import SpinBoxSettingCard


class TwoRunBusinessInterface(ScrollArea):
    """每日任务 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.skillCardData: Dict[str, SpinBoxSettingCard] = {}  # 角色技能卡片集合
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.settingLabel = QLabel("跑商配置", self)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("TwoCityRunnBusinessInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.loadSamples()
        self.__initLayout()
        self.__connectSignalToSlot()

    def loadSamples(self):
        """load samples"""
        self.testRunBusinessCard = PrimaryPushLoadCard(
            "测试", FIF.TAG, "跑商测试", "测试跑商功能", self.scrollWidget
        )
        self.cityCheckboxGroup = CheckboxGroup(self.scrollWidget)
        for city in CITYS:
            checkbox = self.cityCheckboxGroup.addCheckbox(city)
            checkbox.toggled.connect(partial(self.check_checkbox, checkbox))

    def check_checkbox(self, checkbox: CheckBox):
        if self.cityCheckboxGroup.count() > 2:
            checkbox.setChecked(False)  # 取消选中

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.expandLayout.setContentsMargins(36, 0, 36, 0)

        self.expandLayout.addWidget(self.cityCheckboxGroup)
        self.expandLayout.addWidget(self.testRunBusinessCard)

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        self.testRunBusinessCard.clicked.connect(self.runBusiness)

    def runBusiness(self):
        from auto.run_business import two_city_run

        # 获取勾选的城市
        checkbox = [checkbox for checkbox in self.cityCheckboxGroup.checkboxGroup if checkbox.isChecked()]
        buy_city_name = checkbox[0].text()
        sell_city_name = checkbox[1].text()

        signalBus.switchToCard.emit("LoggerInterface")
        self.workers = Worker(
            two_city_run,
            two_city_run,
            buy_city_name=buy_city_name,
            sell_city_name=sell_city_name,
        )
        self.workers.start()
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))

    def on_worker_finished(self, worker: Worker):
        # 线程完成时调用
        self.testRunBusinessCard.loading(False)
        worker and worker.deleteLater()  # 安全删除Worker对象
        self.workers = None
