"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 18:52:36
LastEditTime: 2025-02-10 23:06:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import argparse
import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

import core.utils.logger  # noqa: F401
from app.components.update_message_box import UpdateMessageBox
from core.utils.update.base_update_utils import LatestInfoResponse
from version import __version__

parser = argparse.ArgumentParser(
    prog="黑月无人驾驶更新器",
    description="黑月无人驾驶更新器",
    epilog="黑月无人驾驶更新器帮助文档",
)
parser.add_argument('-cdk', '--mirror_cdk', default="")
parser.add_argument('-data', '--update_data')
args = parser.parse_args()

if os.path.exists("./config/app.json"):
    with open("./config/app.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        mirror_cdk = config.get("Global", {}).get("mirrorCdk", "")
    if not args.mirror_cdk:
        args.mirror_cdk = mirror_cdk

update_data = None
if args.update_data:
    update_data = LatestInfoResponse.model_validate_json(args.update_data)

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
w.cancelButton.clicked.connect(sys.exit)
w.show(args.mirror_cdk, update_data)

app.exec_()
