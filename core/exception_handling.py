"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-03 17:00:41
LastEditTime: 2024-04-22 23:09:43
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from pathlib import Path

import cv2 as cv

from core.adb import input_tap, screenshot
from core.image import crop_image, show_image
from core.ocr import predict

ROOT_PATH = Path()
"""项目根目录路径"""
IMAGE_PATH = ROOT_PATH / "logs" / "image"
"""异常图片文件夹路径"""
IMAGE_PATH.exists() or IMAGE_PATH.mkdir(parents=True, exist_ok=True)


def get_excption():
    timestamp = int(time.time() * 1000)
    image = screenshot()
    cv.imwrite(str(IMAGE_PATH / f"{timestamp}.png"), image)
    if not_strength(image):
        return "澄明度不足"
    if not_negotiate_price(image):
        return "议价次数不足"
    return f"未知异常-{timestamp}"


def not_strength(image):
    image = crop_image(image, (443, 315), (938, 400))
    data = predict(image)
    if not data:
        return False
    if "澄明度不足" in data[0]["text"]:
        input_tap((319, 512))
        return True
    return False


def not_negotiate_price(image):
    image = crop_image(image, (459, 422), (816, 462))
    data = predict(image)
    if not data:
        return False
    if "重新议价" in data[0]["text"]:
        input_tap((319, 512))
        return True
    return False
