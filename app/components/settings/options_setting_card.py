# coding:utf-8
from typing import Union
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QButtonGroup, QLabel

from ...common.config import OptionsConfigItem, qconfig
from ...common.icon import FluentIconBase
from qfluentwidgets import RadioButton
from qfluentwidgets import ExpandSettingCard
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import OptionsSettingCard, ScrollArea, SettingCardGroup

from app.common.config import cfg

from .spin_box_setting_card import SpinBoxSettingCard


class OptionsSettingCard(ExpandSettingCard):
    """setting card with a group of options"""

    optionChanged = pyqtSignal(OptionsConfigItem)

    def __init__(
        self,
        configItem,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        content=None,
        texts=None,
        parent=None,
    ):
        """
        Parameters
        ----------
        configItem: OptionsConfigItem
            options config item

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of setting card

        content: str
            the content of setting card

        texts: List[str]
            the texts of radio buttons

        parent: QWidget
            parent window
        """
        super().__init__(icon, title, content, parent)
        self.texts = texts or []

        self.七号自由港 = SpinBoxSettingCard(
            cfg.七号自由港,
            FIF.ACCEPT,
            "七号自由港",
            "七号自由港单次最大进货书",
            parent=self,
        )
        self.澄明数据中心 = SpinBoxSettingCard(
            cfg.澄明数据中心,
            FIF.ACCEPT,
            "澄明数据中心",
            "澄明数据中心单次最大进货书",
            parent=self,
        )
        self.阿妮塔战备工厂 = SpinBoxSettingCard(
            cfg.阿妮塔战备工厂,
            FIF.ACCEPT,
            "阿妮塔战备工厂",
            "阿妮塔战备工厂单次最大进货书",
            parent=self,
        )
        self.阿妮塔能源研究所 = SpinBoxSettingCard(
            cfg.阿妮塔能源研究所,
            FIF.ACCEPT,
            "阿妮塔能源研究所",
            "阿妮塔能源研究所单次最大进货书",
            parent=self,
        )
        self.淘金乐园 = SpinBoxSettingCard(
            cfg.淘金乐园,
            FIF.ACCEPT,
            "淘金乐园",
            "淘金乐园单次最大进货书",
            parent=self,
        )
        self.曼德矿场 = SpinBoxSettingCard(
            cfg.曼德矿场,
            FIF.ACCEPT,
            "曼德矿场",
            "曼德矿场单次最大进货书",
            parent=self,
        )
        self.荒原站 = SpinBoxSettingCard(
            cfg.荒原站,
            FIF.ACCEPT,
            "荒原站",
            "荒原站单次最大进货书",
            parent=self,
        )
        self.铁盟哨站 = SpinBoxSettingCard(
            cfg.铁盟哨站,
            FIF.ACCEPT,
            "铁盟哨站",
            "铁盟哨站单次最大进货书",
            parent=self,
        )
        self.修格里城 = SpinBoxSettingCard(
            cfg.修格里城,
            FIF.ACCEPT,
            "修格里城",
            "修格里城单次最大进货书",
            parent=self,
        )
        self.priceThreshold = SpinBoxSettingCard(
            cfg.priceThreshold,
            FIF.ACCEPT,
            "价格阈值",
            "低价值商品统计阈值",
            spin_box_min=0,
            spin_box_max=1000,
            parent=self,
        )

        self.viewLayout.setSpacing(19)
        self.viewLayout.setContentsMargins(48, 18, 0, 18)

        self.viewLayout.addWidget(self.七号自由港)
        self.viewLayout.addWidget(self.澄明数据中心)
        self.viewLayout.addWidget(self.阿妮塔战备工厂)
        self.viewLayout.addWidget(self.阿妮塔能源研究所)
        self.viewLayout.addWidget(self.淘金乐园)
        self.viewLayout.addWidget(self.曼德矿场)
        self.viewLayout.addWidget(self.荒原站)
        self.viewLayout.addWidget(self.铁盟哨站)
        self.viewLayout.addWidget(self.修格里城)
        self.viewLayout.addWidget(self.priceThreshold)
        self._adjustViewSize()
