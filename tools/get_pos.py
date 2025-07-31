"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-25 23:03:03
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-02-11 21:03:19
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import cv2

from core.control.control import connect, screenshot, screenshot_image

connect()


# 定义鼠标点击事件处理函数
def click_event(event, x, y, flags, param):
    global zoom_mode, original_image
    zoomed_x = param["zoomed_x"]
    zoomed_y = param["zoomed_y"]
    image = param["image"]
    amplify = param["amplify"]
    # 检查事件是否为左键点击
    if event == cv2.EVENT_LBUTTONDOWN:
        color = image[y, x]
        color_bgr = color.tolist()
        color_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[y, x].tolist()
        if amplify:
            print("Clicked at: ", (int(x/5) + zoomed_x, int(y/5) + zoomed_y))
        else:
            print("Clicked at: ", (x + zoomed_x, y + zoomed_y))
        print("Color (BGR): ", f"({color_bgr[0]}, {color_bgr[1]}, {color_bgr[2]})")
        print("Color (HSV): ", f"({color_hsv[0]}, {color_hsv[1]}, {color_hsv[2]})")

        # 放大模式下显示点击区域的放大图
        if zoom_mode:
            zoomed_y = max(0, y - 50)
            zoomed_x = max(0, x - 50)
            print(zoomed_x, zoomed_y)
            # 获取区域的边界
            zoomed_area = original_image[
                zoomed_y : min(y + 50, original_image.shape[0]),
                zoomed_x : min(x + 50, original_image.shape[1]),
            ]
            # 放大5倍
            zoomed_image = cv2.resize(
                zoomed_area, (zoomed_area.shape[1] * 5, zoomed_area.shape[0] * 5)
            )

            # 显示放大区域
            cv2.imshow("Zoomed Area", zoomed_image)
            cv2.setMouseCallback(
                "Zoomed Area",
                click_event,
                param={
                    "zoomed_x": zoomed_x,
                    "zoomed_y": zoomed_y,
                    "image": zoomed_image,
                    "amplify": True
                },
            )


# 全局变量
zoom_mode = False  # 放大模式开关
original_image = screenshot_image()

cv2.namedWindow("image")
cv2.setMouseCallback(
    "image",
    click_event,
    param={
        "zoomed_x": 0,
        "zoomed_y": 0,
        "image": original_image,
        "amplify": False
    },
)

while True:
    cv2.imshow("image", original_image)

    # 等待键盘事件
    key = cv2.waitKey(1) & 0xFF

    # 按 'C' 键切换放大模式
    if key == ord("c"):
        zoom_mode = not zoom_mode
        print("Zoom mode:", "ON" if zoom_mode else "OFF")

    # 按 'q' 键退出
    if key == ord("q"):
        break

    if key == ord("r"):
        original_image = screenshot_image()
        zoom_mode = False
        break

cv2.destroyAllWindows()
