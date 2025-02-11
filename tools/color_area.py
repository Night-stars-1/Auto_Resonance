"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2025-02-11 17:06:05
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-02-11 18:33:45
"""

import sys
from pathlib import Path

import numpy as np

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import cv2

from core.adb.adb import connect, screenshot

connect(16384)

screenshot_cv = screenshot()

# 设置HSV范围
lower_color = np.array([100, 30, 170])
upper_color = np.array([110, 60, 220])

hsv_image = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)

# 创建指定像素掩码
mask = cv2.inRange(hsv_image, lower_color, upper_color)

# 调整阈值以影响精度
mask = cv2.GaussianBlur(mask, (5, 5), 0)

# 找到指定区域的连通区域
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result_image = screenshot_cv.copy()

# 绘制每个连通区域
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # if h < 10 or w < 10:
    #     continue
    # 计算该区域的蓝色像素数量
    blue_pixels_in_contour = cv2.countNonZero(mask[contour[:, 0, 1], contour[:, 0, 0]])

    # 计算区域的总像素数量
    total_area_pixels = cv2.contourArea(contour)
    if blue_pixels_in_contour < 40:
        continue
    print(f"区域的像素数量: {blue_pixels_in_contour}")
    print(f"区域的总像素数量: {total_area_pixels}")
    print("----------------------------------------------")
    # cv2.drawContours(result_image, [contour], -1, (0, 255, 0), 2)
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(
        result_image,
        f"{blue_pixels_in_contour}",
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
    )

cv2.imshow("Color Area", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
