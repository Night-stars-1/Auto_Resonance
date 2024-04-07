"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-03 17:00:41
LastEditTime: 2024-04-05 18:06:10
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from core.adb import input_tap, screenshot
from core.image import crop_image, show_image
from core.ocr import predict


def get_excption():
    image = screenshot()
    if not_strength(image):
        return "澄明度不足"
    if not_negotiate_price(image):
        return "议价次数不足"
    return "未知异常"


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
