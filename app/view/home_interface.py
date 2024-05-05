"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 19:12:22
LastEditTime: 2024-05-04 17:07:15
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import QRectF, Qt, QTimer
from PyQt5.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPainterPath, QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon, ScrollArea, isDarkTheme
from qfluentwidgets.window.stacked_widget import StackedWidget

from core.api.srap import get_boss

from ..common.config import REPO_URL, cfg
from ..common.style_sheet import StyleSheet
from ..common.worker import Worker
from ..components.button_card import ButtonCardView
from ..components.homes.title_brogress_bars_card import TitleProgressBarsCard
from ..components.link_card import LinkCardView
from ..components.settings.checkbox_group_card import CheckboxGroup


class BannerWidget(QWidget):
    """Banner widget"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.titleLabel = QLabel("黑月无人驾驶", self)
        self.banner = QPixmap(":/gallery/images/header1.png")
        self.linkCardView = LinkCardView(self)

        self.__initWidget()
        self.loadSamples()

        self.worker = Worker(get_boss, get_boss)
        self.worker.result.connect(self.updateProgress)

        # 初始化定时器
        QTimer.singleShot(0, self.startUpdatingProgress)  # 手动触发一次
        self.timer = QTimer(self)
        self.timer.setInterval(10000)  # 设置定时器周期为10000毫秒（10秒）
        self.timer.timeout.connect(self.startUpdatingProgress)  # 连接定时器信号到槽函数
        self.timer.start()  # 启动定时器

    def __initWidget(self):
        self.titleLabel.setObjectName("galleryLabel")

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def loadSamples(self):
        self.linkCardView.addCard(
            FluentIcon.GITHUB, "GitHub repo", "黑月无人驾驶", REPO_URL
        )

        self.bossCard = TitleProgressBarsCard(
            "世界BOSS信息", [], self.linkCardView.view
        )
        self.linkCardView.hBoxLayout.addWidget(self.bossCard, 0, Qt.AlignLeft)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()  # 窗口的宽度和高度
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

        # 绘制图片
        pixmap = self.banner.scaled(self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))

    def startUpdatingProgress(self):
        if not self.worker.isRunning():  # 如果Worker线程未运行，则启动它
            self.worker.start()

    def updateProgress(self, boss_data):
        stackedWidget: StackedWidget = self.window().stackedWidget
        if stackedWidget.currentIndex() == 0:
            self.bossCard.setValue(boss_data)


class HomeInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.workers: Worker = None  # 用于存储活动的 Worker 实例

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

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """load samples"""
        # basic input samples
        basicInputView = ButtonCardView(
            "开始运行", header=self.taskCheckboxGroup, parent=self.view
        )

        self.taskCheckboxGroup.addCheckbox("购买桦石", cfg.huashi)
        self.taskCheckboxGroup.addCheckbox("刷铁安局", cfg.railwaySafetyBureau)
        self.taskCheckboxGroup.addCheckbox("自动跑商", cfg.runBusiness)

        self.run = basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="运行",
            content="运行测试版本",
            func=self._run,
            routekey="LoggerInterface",
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="停止",
            content="停止运行",
            func=self._stop,
            routekey="LoggerInterface",
        )

        self.vBoxLayout.addWidget(basicInputView)

    def _run(self):
        """运行自动化程序"""
        if self.run.titleLabel.text() == "运行":
            self.run.titleLabel.setText("停止")
            from main import main, stop

            tasks = self.taskCheckboxGroup.getAllAccept()
            self.workers = Worker(main, stop, tasks=tasks)
            self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))
            self.workers.start()
        else:
            self.workers.stop()

    def _stop(self):
        """停止自动化程序"""
        from main import main, stop

        self.workers = Worker(main, stop)
        self.workers.finished.connect(lambda: self.on_worker_finished(self.workers))
        self.workers.stop()

    def on_worker_finished(self, worker: Worker):
        # 线程完成时调用
        self.run.titleLabel.setText("运行")
        worker.deleteLater()  # 安全删除Worker对象
        self.workers = None
