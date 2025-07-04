"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 18:52:36
LastEditTime: 2025-02-10 23:06:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
from app.common.utils import save_json, read_json
data = read_json("config/app.json")
# 兼容1.4.4版本错误
if data.get("Global", {}).get("adbPort") is not None and not isinstance(
    data["Global"]["adbPort"], str
):
    data["Global"]["adbPort"] = str(data["Global"]["adbPort"])
    save_json("config/app.json", data)

import atexit
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from app.common.config import cfg

cfg.save()  # 生成配置文件
from app.view.main_window import MainWindow
from core.adb.adb import kill


def close_service():
    """界面退出关闭服务"""
    kill()


def exception_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)  # 强制程序退出


sys.excepthook = exception_hook  # 设置全局异常钩子
atexit.register(close_service)  # 注册退出时的清理函数

# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# create main window
w = MainWindow()
import main

w.show()

app.exec_()
