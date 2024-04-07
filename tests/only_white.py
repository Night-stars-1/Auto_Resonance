"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 18:50:23
LastEditTime: 2024-04-05 21:19:34
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 22:14:42
LastEditTime: 2024-04-05 18:44:40
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
import time
from pathlib import Path

import cv2
import numpy as np

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from core.adb import connect, screenshot
from core.image import crop_image, show_image

connect()


def get_all_station():
    all_pos = []
    image = screenshot()
    image = crop_image(image, cropped_pos1=(0, 66), cropped_pos2=(1280, 720))
    # 转换到灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 设置白色的阈值范围
    threshold_lower = 200
    threshold_upper = 255

    # 阈值处理找到白色区域
    _, thresh = cv2.threshold(gray, threshold_lower, threshold_upper, cv2.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        # 只处理指定面积的轮廓
        if 50 < area < 200:
            # 计算每个轮廓的边界框
            x, y, w, h = cv2.boundingRect(contour)
            pos = (x + w / 2, y + h / 2)
            print(f"区间坐标: {pos}, 宽度:{w}, 高度:{h} 数量: {area}")

            # 可选：在原图上绘制边界框，以可视化结果
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                image,
                f"{area}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
    return image


# 显示带有边界框的图像，以便验证
cv2.imshow("White Areas Bounding Boxes", get_all_station())
cv2.waitKey(0)
cv2.destroyAllWindows()
