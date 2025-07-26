"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 22:14:42
LastEditTime: 2024-04-05 18:44:40
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from core.control.control import connect, screenshot
from core.image.image import crop_image, show_image
from core.image.ocr import predict

connect()
image = screenshot()
image = crop_image(image, cropped_pos1=(0, 66), cropped_pos2=(1280, 720))
show_image(image)
data = predict(image)
# 计算每个文本框的中心点坐标
centers = {}
for item in data:
    position = item["position"]
    # 计算中心点坐标
    center_x = (position[0][0] + position[2][0]) / 2
    center_y = (position[0][1] + position[2][1]) / 2
    centers[item["text"]] = (center_x, center_y)
    for center, pos in centers.copy().items():
        if abs(center_x - pos[0]) < 50 and pos != (center_x, center_y):
            centers.pop(center)
            if item["text"] in centers:
                centers.pop(item["text"])
            centers[center + item["text"]] = (center_x, center_y)

print(centers)
