"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:06:19
LastEditTime: 2024-04-04 19:13:17
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import cv2
import numpy as np

from core.adb import connect, screenshot
from core.image import show_image

connect()

image = screenshot()
start = time.perf_counter()
lower_color_bound = np.array([36, 36, 36])
upper_color_bound = np.array([36, 36, 36])

# 指定区间 (y坐标，x起始坐标，x结束坐标)
y = 418  # 例如，我们只考虑y=50这一行
x_start = 872
x_end = 1240

# 获取指定行的指定区间
row_segment = image[y : y + 1, x_start:x_end]
# show_image(row_segment)
# 寻找指定颜色
mask = cv2.inRange(row_segment, lower_color_bound, upper_color_bound)

# 计算指定颜色的长度

color_length = np.sum(mask == 255) / (x_end - x_start)
print(np.sum(mask == 255), (x_end - x_start))
print(f"指定颜色的长度（像素）: {1-color_length}")
print(f"耗时: {time.perf_counter()-start}")
