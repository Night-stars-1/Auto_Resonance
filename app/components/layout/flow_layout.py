"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-12-28 00:43:11
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2024-12-28 01:10:06
"""

from PyQt5.QtCore import QRect, QSize, pyqtSignal
from PyQt5.QtWidgets import QLayout


class FlowLayout(QLayout):
    layoutChanged = pyqtSignal()  # 信号，用于通知布局发生了变化

    def __init__(self, parent=None):
        super().__init__(parent)
        self._spacing = 0  # 控件间的间距
        self._items = []  # 存储布局中的子控件

    def setSpacing(self, spacing):
        """设置控件间的间距"""
        self._spacing = spacing

    def addItem(self, item):
        """添加一个控件到布局"""
        self._items.append(item)

    def count(self):
        """返回布局中的控件数量"""
        return len(self._items)

    def itemAt(self, index):
        """返回指定索引位置的控件"""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        """移除并返回指定索引位置的控件"""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def sizeHint(self):
        """返回布局的推荐大小"""
        return self._calculateSize()

    def minimumSize(self):
        """返回布局的最小大小"""
        return self._calculateSize()

    def setGeometry(self, rect):
        """对子控件进行布局"""
        super().setGeometry(rect)
        x, y, lineHeight = rect.x(), rect.y(), 0

        for item in self._items:
            widgetSize = item.sizeHint()
            nextX = x + widgetSize.width() + self._spacing

            if nextX - self._spacing > rect.right():  # 如果超出布局区域宽度，则换行
                x = rect.x()
                y += lineHeight + 5
                lineHeight = 0

            item.setGeometry(QRect(x, y, widgetSize.width(), widgetSize.height()))
            x += widgetSize.width() + self._spacing
            lineHeight = max(lineHeight, widgetSize.height())
        self.layoutChanged.emit()  # 发出布局改变的信号

    def _calculateSize(self):
        """计算布局的推荐大小或最小大小"""
        width, height, lineHeight = 0, 0, 0

        for item in self._items:
            widgetSize = item.sizeHint()
            if width + widgetSize.width() + self._spacing > self.geometry().width():
                height += lineHeight + self._spacing
                lineHeight = widgetSize.height()
                width = widgetSize.width()
            else:
                width += widgetSize.width() + self._spacing
                lineHeight = max(lineHeight, widgetSize.height())

        height += lineHeight  # 添加最后一行高度
        return QSize(width, height)
