"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:06:19
LastEditTime: 2024-05-04 15:03:42
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import cv2

from core.adb import connect, screenshot

connect("127.0.0.1:16384")


# 澄明数据中心 (1049, 345) 7号自由港 (665, 577) 阿妮塔战备工厂 (832, 664) 阿妮塔发射中心 (164, 420+577) 阿妮塔能源研究所 (614, 454+577)
# 修格里城 (285+1049, 121+345) 铁盟哨站 (501+1049, 122+345) 荒原站 (753+1049, 121+345)
# 曼德矿场 (602+1049, 322+345) 淘金乐园 (701+1049, 604+345)
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
# image = cv2.imread("resources/test/MuMu12-20240422-002758.png")
"""
Clicked at:  (626, 273)
Color (BGR):  [181, 199, 14]
Color (HSV):  [33, 237, 199]
Clicked at:  (636, 267)
Color (BGR):  [178, 193, 11]
Color (HSV):  [32, 240, 193]
Clicked at:  (609, 289)
Color (BGR):  [182, 195, 12]
Color (HSV):  [32, 239, 195]

Clicked at:  (632, 267)
Color (BGR):  [50, 69, 200]
Color (HSV):  [116, 191, 200]
Clicked at:  (626, 275)
Color (BGR):  [46, 66, 196]
Color (HSV):  [116, 195, 196]
Clicked at:  (612, 286)
Color (BGR):  [49, 65, 191]
Color (HSV):  [117, 190, 191]
"""
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_event, param=image)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
