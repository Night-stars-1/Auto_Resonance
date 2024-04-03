"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 22:14:42
LastEditTime: 2024-04-03 13:28:39
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import math

from core.adb import connect, screenshot
from core.image import crop_image, show_image
from core.ocr import predict

connect()
image = screenshot()
image = crop_image(image, (731, 850, 148, 680))
# show_image(image)
data = predict(image)
centers = set()
for center in data:
    if center["text"][int(len(center["text"]) / 2)] not in "0123456789":
        centers.add(center["text"])
print(centers)
