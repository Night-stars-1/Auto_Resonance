"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 18:52:36
LastEditTime: 2025-02-10 23:06:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import atexit
import sys

from PySide6.QtWidgets import QApplication

from app.common.config import cfg

cfg.save()  # 生成配置文件
from app.view.main_window import MainWindow
from core.control.control import kill


def close_service():
    """界面退出关闭服务"""
    kill()


def exception_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)  # 强制程序退出


sys.excepthook = exception_hook  # 设置全局异常钩子
atexit.register(close_service)  # 注册退出时的清理函数


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
