from typing import Dict, List, Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QFrame, QWidget
from qfluentwidgets import ProgressBar, TitleLabel, TextWrap


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
    """标题进度条列表"""

    def __init__(self, title: str, data: List[Dict[str, Union[str, int]]], parent=None):
        super().__init__(parent=parent)
        self.titleProgressBarWidgets: Dict[str, TitleProgressBar] = {} # 用于存储标题和对应的进度条

        # 总布局
        self.vBoxLayout = QVBoxLayout(self)

        # 标题
        self.titleLabel = TitleLabel(title, self)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)

        # 为每个标题和进度条创建水平布局
        for progress_data in data:
            titleProgressBar = TitleProgressBar(progress_data["title"], progress_data["content"], progress_data["progress"])
            self.vBoxLayout.addWidget(titleProgressBar)
        self.setFixedSize(400, 220)

    def setValue(self, data: List[Dict[str, Union[str, int]]]):
        # 创建一个集合来存储新数据中所有的标题
        current_titles = {item['title'] for item in data}
        
        # 找出需要删除的进度条
        titles_to_remove = [title for title in self.titleProgressBarWidgets if title not in current_titles]
        for title in titles_to_remove:
            # 移除进度条控件
            widget_to_remove = self.titleProgressBarWidgets[title]
            self.vBoxLayout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()  # 删除QWidget，释放资源
            del self.titleProgressBarWidgets[title]  # 从字典中删除记录

        # 现在处理新的或需要更新的数据
        for progress_data in data:
            title = progress_data['title']
            content = progress_data['content']
            progress = progress_data['progress']
            if title in self.titleProgressBarWidgets:
                # 更新已存在的进度条
                self.titleProgressBarWidgets[title].progressBar.setValue(progress)
            else:
                # 创建新的进度条并添加到布局中
                new_title_progress_bar = TitleProgressBar(title, content, progress, self)
                self.vBoxLayout.addWidget(new_title_progress_bar)
                self.titleProgressBarWidgets[title] = new_title_progress_bar

