import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import cv2
import numpy as np
from core.adb import connect, screenshot

# 加载图像
connect()
image = screenshot()
cropped_pos1 = (4, 91)
cropped_pos2 = (1276, 714)
image = image[cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]]
# 将BGR图像转换为HSV颜色空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 紫色在HSV空间中的范围
# 注意：这些值可能需要根据你的具体需求进行调整
lower_purple = np.array([105, 254, 95])
upper_purple = np.array([108, 255, 100])

# 获取紫色区域的掩码
mask = cv2.inRange(hsv, lower_purple, upper_purple)

# 可选：使用掩码来提取紫色区域
purple_area = cv2.bitwise_and(image, image, mask=mask)

# 获取紫色像素的坐标
y_coords, x_coords = np.where(mask == 255)

# 在紫色像素上标记（例如，用红色圆圈标记）
for x, y in zip(x_coords, y_coords):
    cv2.circle(image, (x, y), radius=1, color=(0, 0, 255), thickness=-1)

# 或者，如果你只想标记中心点或某些特定点
# 你可以计算坐标的平均值来找到一个"中心点"
if len(x_coords) > 0 and len(y_coords) > 0:
    cx = np.mean(x_coords).astype(int)
    cy = np.mean(y_coords).astype(int)
    cv2.drawMarker(
        image,
        (cx, cy),
        color=(0, 255, 0),
        markerType=cv2.MARKER_CROSS,
        markerSize=20,
        thickness=2,
    )

window_size = (10, 10)  # 窗口大小，例如50x50像素
threshold = 2000  # 紫色像素的最小数量阈值

# 图像尺寸
height, width = mask.shape

# 遍历图像
for y in range(0, height - window_size[1] + 1, 10):  # 步长为10，可调整
    for x in range(0, width - window_size[0] + 1, 10):
        # 计算当前窗口内紫色像素的数量
        window = mask[y : y + window_size[1], x : x + window_size[0]]
        purple_count = cv2.countNonZero(window)

        # 如果紫色像素的数量达到阈值
        if 20 <= purple_count <= 40:
            # 绘制矩形框，标记这个区域
            cv2.rectangle(
                image, (x, y), (x + window_size[0], y + window_size[1]), (0, 255, 0), 2
            )

# 显示结果
cv2.imshow("Original Image", image)
# cv2.imshow('Mask', mask)
# cv2.imshow('Purple Area', purple_area)

cv2.waitKey(0)
cv2.destroyAllWindows()
