"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:06:19
LastEditTime: 2024-04-01 23:15:25
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import cv2

from core.adb import connect, screenshot

connect()


def click_event(event, x, y, flags, param):
    # 检查事件是否为左键点击
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Clicked at: ", (x, y))


screenshot = screenshot()


cv2.namedWindow("image")
cv2.setMouseCallback("image", click_event)
cv2.imshow("image", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
