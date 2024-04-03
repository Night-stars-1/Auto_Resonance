"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 18:13:56
LastEditTime: 2024-04-03 00:09:33
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
# show_image(image)
data = predict(image)
print(data)
