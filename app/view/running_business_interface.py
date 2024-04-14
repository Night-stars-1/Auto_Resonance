"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-10 22:54:08
LastEditTime: 2024-04-14 16:08:08
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import Dialog, ExpandLayout, ExpandSettingCard
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PrimaryPushSettingCard, ScrollArea

from core.goods.kmou import get_goods_info as get_goods_info_kmou
from core.goods.srap import get_goods_info as get_goods_info_srap

from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..common.worker import Worker
from ..components.settings.spin_box_setting_card import SpinBoxSettingCard

SKILLS = [
    "朱利安",
    "狮鬃",
    "魇",
    "塞西尔",
    "雷火",
    "黛丝莉",
    "艾略特",
    "多萝西",
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
    "卡洛琳",
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
]
STATIONS = [
    "七号自由港",
    "澄明数据中心",
    "曼德矿场",
    "修格里城",
]


class RunningBusinessInterface(ScrollArea):
    """每日任务 interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
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

        self.maxGoodsNum = SpinBoxSettingCard(
            cfg.maxGoodsNum,
            FIF.ACCEPT,
            "最大商品数量",
            "最大商品数量",
            spin_box_min=0,
            spin_box_max=1000,
            parent=self.scrollWidget,
        )
        self.testCard = PrimaryPushSettingCard(
            "测试", FIF.TAG, "跑商测试", "测试跑商功能", self.scrollWidget
        )
        self.bookGroup = ExpandSettingCard(
            FIF.BRUSH, "进货书设置", parent=self.scrollWidget
        )
        for city in CITYS:
            book = SpinBoxSettingCard(
                getattr(cfg, f"{city}进货书"),
                FIF.ACCEPT,
                city,
                f"{city}单次最大进货书",
                parent=self.bookGroup,
            )
            self.bookGroup.viewLayout.addWidget(book)
        self.priceThreshold = SpinBoxSettingCard(
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
        for skill in SKILLS:
            gz = SpinBoxSettingCard(
                getattr(cfg, skill),
                FIF.ACCEPT,
                skill,
                f"{skill}共振等级",
                spin_box_min=0,
                spin_box_max=5,
                parent=self.skillGroup,
            )
            self.skillGroup.viewLayout.addWidget(gz)

        self.tiredGroup = ExpandSettingCard(
            FIF.BRUSH, "进货书设置", parent=self.scrollWidget
        )
        for city in CITYS:
            book = SpinBoxSettingCard(
                getattr(cfg, f"{city}砍抬疲劳"),
                FIF.ACCEPT,
                city,
                f"{city}砍抬疲劳",
                parent=self.tiredGroup,
            )
            self.tiredGroup.viewLayout.addWidget(book)

        self.levelGroup = ExpandSettingCard(
            FIF.BRUSH, "声望设置设置", parent=self.scrollWidget
        )
        for station in STATIONS:
            book = SpinBoxSettingCard(
                getattr(cfg, f"{station}声望"),
                FIF.ACCEPT,
                station,
                f"{station}声望",
                parent=self.levelGroup,
            )
            self.levelGroup.viewLayout.addWidget(book)

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.bookGroup.viewLayout.addWidget(self.priceThreshold)
        self.bookGroup._adjustViewSize()
        self.skillGroup._adjustViewSize()
        self.tiredGroup._adjustViewSize()
        self.levelGroup._adjustViewSize()

        self.bookGroup.setExpand(True)  # 展开进货书折叠栏

        # add setting card group to layout
        # self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 0, 36, 0)
        self.expandLayout.addWidget(self.maxGoodsNum)
        self.expandLayout.addWidget(self.testCard)
        self.expandLayout.addWidget(self.bookGroup)
        self.expandLayout.addWidget(self.skillGroup)
        self.expandLayout.addWidget(self.tiredGroup)
        self.expandLayout.addWidget(self.levelGroup)

    def __connectSignalToSlot(self):
        """connect signal to slot"""
        self.testCard.clicked.connect(self.createSuccessInfoBar)

    def createSuccessInfoBar(self):
        from auto.run_business import run
        from core.goods.shop import show

        city_book = cfg.toDict()["RunningBusiness"]
        skill_level = cfg.toDict()["SkillLevel"]
        station_level = cfg.toDict()["StationLevel"]
        max_goods_num = cfg.maxGoodsNum.value
        uuid = cfg.uuid.value
        if cfg.goodsType.value:
            if uuid == "":
                logger.info("未设置UUID")
                return False
            route = get_goods_info_kmou(
                city_book, skill_level, station_level, max_goods_num, uuid
            )
        else:
            route = get_goods_info_srap(
                city_book, skill_level, station_level, max_goods_num
            )
        w = Dialog("详细", show(route), self)
        if w.exec():
            signalBus.switchToCard.emit("LoggerInterface")
            self.workers = Worker(
                run,
                run,
                city_book=cfg.toDict()["RunningBusiness"],
                skill_level=cfg.toDict()["SkillLevel"],
                station_level=cfg.toDict()["StationLevel"],
                max_goods_num=max_goods_num,
                route=route,
                type_=cfg.goodsType.value,
                uuid=cfg.uuid.value,
            )
            self.workers.start()

        """
        InfoBar.success(
            title="成功",
            content=get_goods_info_kmou(cfg.uuid.value) if cfg.goodsType.value else get_goods_info_srap(),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
        """
