"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:06:19
LastEditTime: 2024-04-11 22:13:04
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import cv2

from core.adb import connect, screenshot

connect("127.0.0.1:21523")


def click_event(event, x, y, flags, param):
    # 检查事件是否为左键点击
    if event == cv2.EVENT_LBUTTONDOWN:
        color = param[y, x]
        color_bgr = color.tolist()  # 将颜色值转换为列表形式
        color_hsv = cv2.cvtColor(param, cv2.COLOR_RGB2HSV)[y, x]
        print("Clicked at: ", (x, y))
        print("Color (BGR): ", color_bgr)
        print("Color (HSV): ", color_hsv.tolist())


image = screenshot()


cv2.namedWindow("image")
cv2.setMouseCallback("image", click_event, param=image)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
