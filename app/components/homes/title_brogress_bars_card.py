"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-20 22:08:58
LastEditTime: 2024-04-21 20:15:56
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict, List, Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import ProgressBar, TextWrap, TitleLabel

from app.common.style_sheet import StyleSheet


class TitleProgressBar(QWidget):
    """标题进度条"""

    def __init__(self, title: str, content: str, progress: int, parent=None):
        super().__init__(parent)

        # 标题标签
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()
        self.titleLabel = QLabel(title, parent)
        self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], parent)
        self.titleLabel.setObjectName(
            title.replace(" ", "_")
        )  # 创建一个基于标题的对象名

        # 进度条
        self.progressBar = ProgressBar(parent)
        self.progressBar.setValue(progress)

        # 将标题和进度条添加到水平布局
        self.hBoxLayout.addWidget(self.titleLabel)
        self.hBoxLayout.addWidget(self.progressBar)
        self.hBoxLayout.setAlignment(
            self.progressBar, Qt.AlignVCenter
        )  # 确保进度条在水平布局中垂直居中
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")

        # 将标题和内容添加到垂直布局
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)


class TitleProgressBarsCard(QFrame):

    def __init__(self, title: str, data: List[Dict[str, Union[str, int]]], parent=None):
        super().__init__(parent=parent)
        self.titleProgressBarWidgets: Dict[str, TitleProgressBar] = (
            {}
        )  # 用于存储标题和对应的进度条

        # 总布局
        self.vBoxLayout = QVBoxLayout(self)

        # 标题
        self.titleLabel = TitleLabel(title, self)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)

        # 滚动布局
        self.scrollArea = QScrollArea(self)
        self.scrollWidget = QFrame(self.scrollArea)
        self.scrollLayout = QVBoxLayout(self.scrollWidget)

        self.scrollWidget.setLayout(self.scrollLayout)

        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.addWidget(self.scrollArea, 0, Qt.AlignCenter)

        # 为每个标题和进度条创建水平布局
        for progress_data in data:
            titleProgressBar = TitleProgressBar(
                progress_data["title"],
                progress_data["content"],
                progress_data["progress"],
            )
            self.scrollLayout.addWidget(titleProgressBar)

        self.setFixedSize(400, 220)
        availableHeight = self.height() - self.titleLabel.height()
        self.scrollArea.setFixedSize(self.width(), availableHeight - 15)

    def setValue(self, data: List[Dict[str, Union[str, int]]]):
        for progress_data in data:
            title = progress_data["title"]
            content = progress_data["content"]
            progress = progress_data["progress"]
            # 如果标题已存在，则更新进度条的值
            if title in self.titleProgressBarWidgets:
                self.titleProgressBarWidgets[title].progressBar.setValue(progress)
            else:
                # 创建新的标题进度条并添加到布局中
                new_title_progress_bar = TitleProgressBar(
                    title, content, progress, self
                )
                self.scrollLayout.addWidget(new_title_progress_bar)
                self.titleProgressBarWidgets[title] = new_title_progress_bar
