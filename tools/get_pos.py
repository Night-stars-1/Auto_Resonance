"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-25 23:03:03
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-02-11 21:03:19
"""

import sys
from pathlib import Path

import numpy as np

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import cv2

from core.control.control import connect, screenshot, screenshot_image

connect()


# 定义鼠标点击事件处理函数
def click_event(event, x, y, flags, param):
    global zoom_mode, zoomed_image, original_image
    # 检查事件是否为左键点击
    if event == cv2.EVENT_LBUTTONDOWN:
        color = param[y, x]
        color_bgr = color.tolist()
        color_hsv = cv2.cvtColor(param, cv2.COLOR_BGR2HSV)[y, x].tolist()
        print("Clicked at: ", (x, y))
        print("Color (BGR): ", f"({color_bgr[0]}, {color_bgr[1]}, {color_bgr[2]})")
        print("Color (HSV): ", f"({color_hsv[0]}, {color_hsv[1]}, {color_hsv[2]})")

        # 放大模式下显示点击区域的放大图
        if zoom_mode:
            # 获取区域的边界
            zoomed_area = original_image[
                max(0, y - 50) : min(y + 50, original_image.shape[0]),
                max(0, x - 50) : min(x + 50, original_image.shape[1]),
            ]
            # 放大2倍
            zoomed_image = cv2.resize(
                zoomed_area, (zoomed_area.shape[1] * 5, zoomed_area.shape[0] * 5)
            )

            # 确保放大后的坐标不会超出放大区域的边界
            zoomed_y = min(y * 2, zoomed_image.shape[0] - 1)  # 防止超出放大图的y轴范围
            zoomed_x = min(x * 2, zoomed_image.shape[1] - 1)  # 防止超出放大图的x轴范围

            # 显示放大区域
            cv2.imshow("Zoomed Area", zoomed_image)
            cv2.setMouseCallback("Zoomed Area", click_event, param=zoomed_image)

            # # 获取放大区域内的颜色值
            # color_zoomed = zoomed_image[zoomed_y, zoomed_x]
            # color_zoomed_bgr = color_zoomed.tolist()
            # color_zoomed_hsv = cv2.cvtColor(np.uint8([[color_zoomed]]), cv2.COLOR_BGR2HSV)[0][0].tolist()
            # print("Zoomed Color (BGR): ", color_zoomed_bgr)
            # print("Zoomed Color (HSV): ", color_zoomed_hsv)


# 全局变量
zoom_mode = False  # 放大模式开关
zoomed_image = None
original_image = screenshot_image()

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_event, param=original_image)

while True:
    cv2.imshow("image", original_image)

    # 等待键盘事件
    key = cv2.waitKey(1) & 0xFF

    # 按 'C' 键切换放大模式
    if key == ord("c"):
        zoom_mode = not zoom_mode  # 切换放大模式
        print("Zoom mode:", "ON" if zoom_mode else "OFF")

    # 按 'q' 键退出
    if key == ord("q"):
        break

cv2.destroyAllWindows()
