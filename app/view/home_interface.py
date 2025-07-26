"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:12:22
LastEditTime: 2025-02-11 19:08:33
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import (
    FluentIcon,
    InfoBar,
    InfoBarIcon,
    InfoBarPosition,
    ScrollArea,
    isDarkTheme,
)

from app.common.config import REPO_URL, cfg
from app.common.style_sheet import StyleSheet
from app.components.button_card import ButtonCardView
from app.components.link_card import LinkCardView
from app.components.settings.checkbox_group_card import CheckboxGroup
from app.utils.constants import ICON_PATH
from core.control.control import stop


class BannerWidget(QWidget):
    """Banner widget"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.titleLabel = QLabel("黑月无人驾驶", self)
        self.banner = QPixmap(ICON_PATH / "header.png")
        self.linkCardView = LinkCardView(self)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.titleLabel.setObjectName("galleryLabel")

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def loadSamples(self):
        self.linkCardView.addCard(
            FluentIcon.GITHUB, "GitHub repo", "黑月无人驾驶", REPO_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # 初始化线性渐变效果
        gradient = QLinearGradient(0, 0, 0, h)

        # 绘制背景颜色
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))

        # # 绘制图片
        pixmap = self.banner.scaled(self.size(), aspectMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, mode=Qt.TransformationMode.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.taskCheckboxGroup = CheckboxGroup(self.view)
        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("HomeInterface")
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def loadSamples(self):
        """load samples"""

        tipBar = InfoBar(
            icon=InfoBarIcon.WARNING,
            title=self.tr("Warning"),
            content="推荐使用 MUMU模拟器 分辨率必须为16:9，推荐: 1920x1080/1280x720",
            orient=Qt.Orientation.Vertical,
            isClosable=False,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self.view,
        )

        basicInputView = ButtonCardView(
            "开始运行", header=self.taskCheckboxGroup, parent=self.view
        )

        basicInputView.vBoxLayout.insertWidget(0, tipBar)
        # self.taskCheckboxGroup.addCheckbox("购买桦石", cfg.huashi)
        # self.taskCheckboxGroup.addCheckbox("刷铁安局", cfg.railwaySafetyBureau)

        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="停止",
            content="停止运行",
            func=stop,
            routekey="LoggerInterface",
        )


        self.vBoxLayout.addWidget(basicInputView)
