"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 18:52:36
LastEditTime: 2024-07-08 23:22:02
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import atexit
import os
import sys

from PyQt5.QtCore import QLocale, Qt, QTranslator
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common.config import cfg

cfg.save()  # 生成配置文件
from app.view.main_window import MainWindow
from core.adb import kill


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

# internationalization
locale = QLocale(QLocale.Chinese, QLocale.China)
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "gallery", ".", "app/resource/i18n")
app.installTranslator(translator)
app.installTranslator(galleryTranslator)

# create main window
w = MainWindow()
from main import run, stop

w.show()

app.exec_()
