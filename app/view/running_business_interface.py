"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2024-05-28 21:04:01
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from qfluentwidgets import Dialog, ExpandLayout, ExpandSettingCard
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ScrollArea

from core.api.kmou import get_goods_info as get_goods_info_kmou
from core.api.srap import get_goods_info as get_goods_info_srap

from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..common.worker import Worker
from ..components.primary_push_load_card import PrimaryPushLoadCard
from ..components.settings.spin_box_setting_card import SpinBoxSettingCard

SKILLS = [
    "朱利安",
    "狮鬃",
    "魇",
    "塞西尔",
    "雷火",
    "黛丝莉",
    "艾略特",
    "静流",
    "多萝西",
    "卡莲",
    "星花",
    "瑞秋",
    "菲妮娅",
    "瓦伦汀",
    "阿知波",
    "闻笙",
    "山岚",
    "叶珏",
    "隼",
    "奈弥",
    "伊尔",
    "甘雅",
    "妮蔻拉",
    "卡洛琳",
    "海因里希",
]
CITYS = [
    "七号自由港",
    "澄明数据中心",
    "阿妮塔战备工厂",
    "阿妮塔能源研究所",
    "淘金乐园",
    "曼德矿场",
    "荒原站",
    "铁盟哨站",
    "修格里城",
    "阿妮塔发射中心",
]
STATIONS = [
    "七号自由港",
    "澄明数据中心",
    "曼德矿场",
    "修格里城",
    "阿妮塔发射中心",
]


class RunningBusinessInterface(ScrollArea):
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
        self.setObjectName("RunningBusinessInterface")

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

        self.maxGoodsNumCard = SpinBoxSettingCard(
            cfg.maxGoodsNum,
            FIF.ACCEPT,
            "最大商品数量",
            "最大商品数量",
            spin_box_min=0,
            spin_box_max=1000,
            parent=self.scrollWidget,
        )
        self.tiredProfitThresholdCard = SpinBoxSettingCard(
            cfg.tiredProfitThreshold,
            FIF.ACCEPT,
            "单位疲劳阈值",
            "当单位疲劳高于该值的时候自动跑商",
            spin_box_max=30000,
            parent=self.scrollWidget,
        )
        self.testRunBusinessCard = PrimaryPushLoadCard(
            "测试", FIF.TAG, "跑商测试", "测试跑商功能", self.scrollWidget
        )
        self.bookGroup = ExpandSettingCard(
            FIF.BRUSH, "进货书设置", parent=self.scrollWidget
        )
        self.totalMaxBookCard = SpinBoxSettingCard(
            cfg.totalMaxBook,
            FIF.ACCEPT,
            "进货书最大使用量",
            "进货书最大使用总量，超过该值不再使用进货书",
            spin_box_min=0,
            spin_box_max=10,
            parent=self.bookGroup,
        )
        self.profitThresholdCard = SpinBoxSettingCard(
            cfg.profitThreshold,
            FIF.ACCEPT,
            "进货书使用阈值",
            "只有利润高于该值的时候才使用进货书",
            spin_box_min=0,
            spin_box_max=500000,
            parent=self.bookGroup,
        )
        self.priceThresholdCard = SpinBoxSettingCard(
            cfg.priceThreshold,
            FIF.ACCEPT,
            "价格阈值",
            "低价值商品统计阈值",
            spin_box_min=0,
            spin_box_max=1000,
            parent=self.bookGroup,
        )

        self.skillGroup = ExpandSettingCard(
            FIF.BRUSH, "共振等级", parent=self.scrollWidget
        )
        # 创建按钮
        self.autoscanreslevel = QPushButton("自动扫描乘员共振等级", self.skillGroup)
        self.skillGroup.viewLayout.addWidget(self.autoscanreslevel)

        for role_name in SKILLS:
            skillCard = SpinBoxSettingCard(
                getattr(cfg, role_name),
                FIF.ACCEPT,
                role_name,
                f"{role_name}共振等级",
                spin_box_min=0,
                spin_box_max=5,
                parent=self.skillGroup,
            )
            self.skillCardData[role_name] = skillCard
            self.skillGroup.viewLayout.addWidget(skillCard)

        self.tiredGroup = ExpandSettingCard(
            FIF.BRUSH,
            "砍抬疲劳设置",
            content="当城市设置砍抬成功次数为-1时禁用该城市",
            parent=self.scrollWidget,
        )
        self.tiredGroup.viewLayout.addWidget(
            SpinBoxSettingCard(
                cfg.buyTired,
                FIF.ACCEPT,
                "单次抬价疲劳",
                "单次砍价疲劳",
                parent=self.tiredGroup,
            )
        )
        self.tiredGroup.viewLayout.addWidget(
            SpinBoxSettingCard(
                cfg.sellTired,
                FIF.ACCEPT,
                "单次抬价疲劳",
                "单次抬价疲劳",
                parent=self.tiredGroup,
            )
        )
        for city in CITYS:
            bookCard = SpinBoxSettingCard(
                getattr(cfg, f"{city}砍抬次数"),
                FIF.ACCEPT,
                city,
                f"{city}砍抬成功次数",
                parent=self.tiredGroup,
                spin_box_min=-1,
            )
            self.tiredGroup.viewLayout.addWidget(bookCard)

        self.levelGroup = ExpandSettingCard(
            FIF.BRUSH, "声望设置设置", parent=self.scrollWidget
        )
        for station in STATIONS:
            bookCard = SpinBoxSettingCard(
                getattr(cfg, f"{station}声望"),
                FIF.ACCEPT,
                station,
                f"{station}声望",
                parent=self.levelGroup,
            )
            self.levelGroup.viewLayout.addWidget(bookCard)

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.bookGroup.viewLayout.addWidget(self.totalMaxBookCard)
        self.bookGroup.viewLayout.addWidget(self.profitThresholdCard)
        self.bookGroup.viewLayout.addWidget(self.priceThresholdCard)
        self.bookGroup._adjustViewSize()
        self.skillGroup._adjustViewSize()
        self.tiredGroup._adjustViewSize()
        self.levelGroup._adjustViewSize()

        # self.bookGroup.setExpand(True)  # 展开进货书折叠栏

        # add setting card group to layout
        # self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 0, 36, 0)
        self.expandLayout.addWidget(self.maxGoodsNumCard)
        self.expandLayout.addWidget(self.tiredProfitThresholdCard)
        self.expandLayout.addWidget(self.testRunBusinessCard)
        self.expandLayout.addWidget(self.bookGroup)
        self.expandLayout.addWidget(self.skillGroup)
        self.expandLayout.addWidget(self.tiredGroup)
        self.expandLayout.addWidget(self.levelGroup)

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        self.testRunBusinessCard.clicked.connect(self.runBusiness)
        self.autoscanreslevel.clicked.connect(self.autoscan)

    def runBusiness(self):
        from auto.run_business import run
        from core.goods import show

        def result(routes):
            w = Dialog("路线详细", show(routes), self)
            if w.exec():
                signalBus.switchToCard.emit("LoggerInterface")
                self.workers = Worker(
                    run,
                    run,
                    routes=routes,
                )
                self.workers.start()
                self.workers.finished.connect(
                    lambda: self.on_worker_finished(self.workers)
                )

        self.testRunBusinessCard.loading(True)

        uuid = cfg.uuid.value
        if cfg.goodsType.value:
            if uuid == "":
                logger.info("未设置UUID")
                return False
            self.workers = Worker(get_goods_info_kmou, get_goods_info_kmou)
            self.workers.start()
            self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))
            self.workers.result.connect(result)
        else:
            self.workers = Worker(get_goods_info_srap, get_goods_info_srap)
            self.workers.start()
            self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))
            self.workers.result.connect(result)

    def autoscan(self):

        def result(skill_level: Dict[str, int]):
            logger.debug(skill_level)
            for role_name in self.skillCardData:
                role_name_other = role_name.replace("闻笙", "闻笔")  # 纠正一些角色名
                self.skillCardData[role_name].spinBox.setValue(
                    skill_level.get(role_name_other, 0)
                )

        signalBus.switchToCard.emit("LoggerInterface")
        from auto.scan_res_level import run

        self.workers = Worker(run, run)
        self.workers.start()
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))
        self.workers.result.connect(result)

    def on_worker_finished(self, worker: Worker):
        # 线程完成时调用
        self.testRunBusinessCard.loading(False)
        worker and worker.deleteLater()  # 安全删除Worker对象
        self.workers = None
