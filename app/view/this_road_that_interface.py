"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2024-04-30 00:35:09
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import ExpandLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea

from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..common.worker import Worker
from ..components.primary_push_load_card import PrimaryPushLoadCard
from ..components.settings.checkbox_group_card import CheckboxGroupCard
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
            "刷取BOSS", FIF.TAG, "BOSS", "清缴任务", parent=self.scrollWidget
        )
        self.bossListGroup = CheckboxGroupCard(
            FIF.TAG, "清缴的BOSS", parent=self.scrollWidget
        )
        self.bossListGroup.addCheckbox("寒潮浮囊体", cfg.thisRoadThatAttackOne)
        self.bossListGroup.addCheckbox("昏恶巨象", cfg.thisRoadThatAttackTwo)
        self.bossListGroup.addCheckbox("尘鸣游磷", cfg.thisRoadThatAttackThree)
        self.bossListGroup.addCheckbox("劫掠者-执桔", cfg.thisRoadThatAttackFour)
        self.bossListGroup.addCheckbox("裂首骨龙", cfg.thisRoadThatAttackFive)

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
        self.thisRoadThatTransportOrderCard = SpinBoxSettingCard(
            cfg.thisRoadThatTransportOrder,
            FIF.ACCEPT,
            "物质运输次数",
            "物质运输次数",
            parent=self.scrollWidget,
        )

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.expandLayout.setContentsMargins(36, 0, 36, 0)
        self.expandLayout.addWidget(self.attackBossCard)
        self.expandLayout.addWidget(self.bossListGroup)
        self.expandLayout.addWidget(self.thisRoadThatBossCard)
        self.expandLayout.addWidget(self.transportOrderCard)
        self.expandLayout.addWidget(self.thisRoadThatTransportOrderCard)

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        self.attackBossCard.clicked.connect(self.clickAttackBoss)
        self.transportOrderCard.clicked.connect(self.clickTransportOrder)

    def clickAttackBoss(self):
        from auto.this_road_that import attack_boss

        self.workers = Worker(
            attack_boss, attack_boss, bossList=self.bossListGroup.getAllAccept()
        )
        self.workers.start()
        signalBus.switchToCard.emit("LoggerInterface")
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))

    def clickTransportOrder(self):
        from auto.this_road_that import transport_order

        self.workers = Worker(transport_order, transport_order)
        self.workers.start()
        signalBus.switchToCard.emit("LoggerInterface")
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))

    def on_worker_finished(self, worker: Worker):
        # 线程完成时调用
        worker and worker.deleteLater()  # 安全删除Worker对象
        self.workers = None
