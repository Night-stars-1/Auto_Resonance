"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 18:52:36
LastEditTime: 2025-02-10 23:06:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from app.components.update_message_box import UpdateMessageBox
from version import __version__

# enable dpi scale
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# create main window
main_window = QMainWindow()
main_window.setWindowIcon(QIcon("./app/resource/images/logo.ico"))
main_window.setWindowTitle(f"黑月无人驾驶更新器 - {__version__}")
main_window.resize(800, 600)
main_window.show()
w = UpdateMessageBox(parent=main_window)
w.cancelButton.clicked.connect(exit)
w.show("")

app.exec_()
