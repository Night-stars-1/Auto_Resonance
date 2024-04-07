"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 22:14:42
LastEditTime: 2024-04-05 19:15:15
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import sys
import time
from pathlib import Path

import cv2 as cv

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from loguru import logger

from core.adb import connect, input_swipe, input_tap, screenshot
from core.image import crop_image, show_image
from core.ocr import predict

connect()
# input_swipe((234, 114), (1101, 627))


def get_all_station():
    all_pos = []
    image = screenshot()
    image = crop_image(image, cropped_pos1=(0, 66), cropped_pos2=(1280, 720))
    # 转换到灰度图
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 设置白色的阈值范围
    threshold_lower = 200
    threshold_upper = 255

    # 阈值处理找到白色区域
    _, thresh = cv.threshold(gray, threshold_lower, threshold_upper, cv.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv.contourArea(contour)

        # 只处理指定面积的轮廓
        if 50 < area < 200:
            # 计算每个轮廓的边界框
            x, y, w, h = cv.boundingRect(contour)
            all_pos.append((x + (w / 2), y + (h / 2) + 66))

    return all_pos


def select_station(name):
    n = 0
    for _ in range(10):
        all_pos = get_all_station()
        for pos in all_pos:
            input_tap(pos)
            time.sleep(0.5)
            image = screenshot()
            data = predict(image, cropped_pos1=(764, 100), cropped_pos2=(1070, 132))
            logger.info([item["text"] for item in data])
            for item in data:
                if name in item["text"]:
                    return
                else:
                    input_tap((86, 415))
                    time.sleep(1)
        if 0 <= n <= 2:
            input_swipe((599, 656), (600, 129), time=500)
            time.sleep(0.5)
        elif n == 3:
            input_swipe((1000, 404), (140, 415), time=500)
            time.sleep(0.5)
        elif 3 > n > 6:
            input_swipe((600, 129), (599, 656), time=500)
            time.sleep(0.5)
        else:
            input_swipe((140, 415), (1000, 404), time=500)
            time.sleep(0.5)
        n += 1


click_station("淘金乐园")
