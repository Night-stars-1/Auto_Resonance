"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2024-04-26 12:51:55
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from qfluentwidgets import Dialog, ExpandLayout, ExpandSettingCard
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PrimaryPushSettingCard, ScrollArea

from core.api.kmou import get_goods_info as get_goods_info_kmou
from core.api.srap import get_goods_info as get_goods_info_srap

from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..common.worker import Worker
from ..components.primary_push_load_card import PrimaryPushLoadCard
from ..components.settings.spin_box_setting_card import SpinBoxSettingCard


class ThisRoadThatInterface(ScrollArea):
    """我建我路 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.settingLabel = QLabel("我建我路", self)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("ThisRoadThatInterface")

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

        self.attackBossCard = PrimaryPushLoadCard(
            "刷取BOSS", FIF.TAG, "BOSS", "清缴任务", self.scrollWidget
        )
        self.thisRoadThatBossCard = SpinBoxSettingCard(
            cfg.thisRoadThatBoss,
            FIF.ACCEPT,
            "刷取BOSS次数",
            "每个BOSS刷取次数",
            parent=self.scrollWidget,
        )
        self.transportOrderCard = PrimaryPushLoadCard(
            "运行物质任务", FIF.TAG, "物质任务", "物质任务", self.scrollWidget
        )

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.expandLayout.setContentsMargins(36, 0, 36, 0)
        self.expandLayout.addWidget(self.attackBossCard)
        self.expandLayout.addWidget(self.thisRoadThatBossCard)
        self.expandLayout.addWidget(self.transportOrderCard)

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        self.attackBossCard.clicked.connect(self.clickAttackBoss)
        self.transportOrderCard.clicked.connect(self.clickTransportOrder)

    def clickAttackBoss(self):
        from auto.this_road_that import attack_boss

        self.workers = Worker(
            attack_boss,
            attack_boss,
            num=cfg.thisRoadThatBoss.value,
        )
        self.workers.start()
        signalBus.switchToCard.emit("LoggerInterface")
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))

    def clickTransportOrder(self):
        from auto.this_road_that import transport_order

        self.workers = Worker(
            transport_order,
            transport_order,
        )
        self.workers.start()
        signalBus.switchToCard.emit("LoggerInterface")
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))

    def on_worker_finished(self, worker: Worker):
        # 线程完成时调用
        worker and worker.deleteLater()  # 安全删除Worker对象
        self.workers = None
