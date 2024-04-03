"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 22:14:42
LastEditTime: 2024-04-03 21:29:45
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from core.adb import connect, screenshot
from core.image import crop_image, show_image
from core.ocr import predict

connect()
image = screenshot()
image = crop_image(image, (443, 938, 315, 400))
# show_image(image)
data = predict(image)
if "澄明度不足" in data[0]["text"]:
    print("澄明度不足")
