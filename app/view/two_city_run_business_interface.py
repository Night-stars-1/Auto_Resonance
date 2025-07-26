"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2025-02-10 23:25:35
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from functools import partial
from typing import Dict, Optional

from loguru import logger
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from qfluentwidgets import CheckBox, ExpandLayout, ExpandSettingCard
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea, InfoBar

from app.common.config import cfg
from app.common.signal_bus import signalBus
from app.common.style_sheet import StyleSheet
from app.utils.worker import Worker
from app.components.primary_push_load_card import PrimaryPushLoadCard
from app.components.settings.checkbox_group_card import CheckboxGroup
from app.components.settings.spin_box_setting_card import SpinBoxSettingCard
from app.utils.config import CITYS


class TwoRunBusinessInterface(ScrollArea):
    """每日任务 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.skillCardData: Dict[str, SpinBoxSettingCard] = {}  # 角色技能卡片集合
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.titleLabel = QLabel("跑商配置", self)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("TwoCityRunnBusinessInterface")

        # initialize style sheet
        self.scrollWidget.setObjectName("scrollWidget")
        self.titleLabel.setObjectName("titleLabel")
        StyleSheet.VIEW_INTERFACE.apply(self)

        # initialize layout
        self.loadSamples()
        self.__initLayout()
        self.connectSignalToSlot()

    def loadSamples(self):
        """load samples"""
        self.testRunBusinessCard = PrimaryPushLoadCard(
            "测试", FIF.TAG, "跑商测试", "测试跑商功能", self.scrollWidget
        )
        self.buyCountCard = SpinBoxSettingCard(
            cfg.BuyCount,
            FIF.ACCEPT,
            "运行次数",
            spin_box_max=20,
            parent=self.scrollWidget,
        )
        self.cityCheckboxGroup = CheckboxGroup(self.scrollWidget)
        for city in CITYS:
            checkbox = self.cityCheckboxGroup.addCheckbox(city)
            checkbox.toggled.connect(partial(self.check_checkbox, checkbox))

        self.bookGroup = ExpandSettingCard(
            FIF.EDIT, "进货书设置", parent=self.scrollWidget
        )
        self.haggleGroup = ExpandSettingCard(
            FIF.EDIT, "议价设置", parent=self.scrollWidget
        )
        for city in CITYS:
            bookCard = SpinBoxSettingCard(
                getattr(cfg, f"{city}进货书"),
                FIF.PENCIL_INK,
                city,
                f"{city}进货书",
                spin_box_max=20,
                parent=self.bookGroup,
            )
            self.bookGroup.viewLayout.addWidget(bookCard)
            haggleCard = SpinBoxSettingCard(
                getattr(cfg, f"{city}议价次数"),
                FIF.PENCIL_INK,
                city,
                f"{city}议价次数",
                spin_box_max=20,
                parent=self.haggleGroup,
            )
            self.haggleGroup.viewLayout.addWidget(haggleCard)

    def check_checkbox(self, checkbox: CheckBox, checked: bool):
        if self.cityCheckboxGroup.count() > 2:
            checkbox.setChecked(False)

    def __initLayout(self):
        self.titleLabel.move(36, 30)

        self.bookGroup._adjustViewSize()
        self.haggleGroup._adjustViewSize()

        self.expandLayout.setContentsMargins(36, 0, 36, 0)

        self.expandLayout.addWidget(self.cityCheckboxGroup)
        self.expandLayout.addWidget(self.testRunBusinessCard)
        self.expandLayout.addWidget(self.buyCountCard)
        self.expandLayout.addWidget(self.bookGroup)
        self.expandLayout.addWidget(self.haggleGroup)

    def connectSignalToSlot(self):
        self.testRunBusinessCard.clicked.connect(self.runBusiness)

    def runBusiness(self):
        from auto.run_business import two_city_run

        # 获取勾选的城市
        checkbox = [
            checkbox
            for checkbox in self.cityCheckboxGroup.checkboxGroup
            if checkbox.isChecked()
        ]
        if len(checkbox) != 2:
            logger.error("请选择两个城市进行跑商")
            InfoBar.warning(
                title='',
                content="请选择两个城市进行跑商",
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                parent=self
            )
            return
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

    def on_worker_finished(self, worker: Optional[Worker]):
        # 线程完成时调用
        self.testRunBusinessCard.loading(False)
        if worker:
            worker.deleteLater()
        self.workers = None
