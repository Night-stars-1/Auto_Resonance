"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2024-04-06 01:48:11
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import random
from subprocess import DEVNULL, run

import cv2 as cv
import numpy as np

ADBOREDER = ""
ADBPATH = ""
EXCURSIONX = [-10, 10]
EXCURSIONY = [-10, 10]


def connect(order="127.0.0.1:7555", path="core\\lib\\adb"):
    """
    说明:
        连接ADB
    参数:
        :param order: ADB端口
    """
    global ADBOREDER, ADBPATH
    ADBOREDER = order
    ADBPATH = path
    shell = [ADBPATH, "connect", ADBOREDER]
    result = run(shell, shell=True, capture_output=True, check=False)
    return "already connected" in str(result.stdout) or "connected to" in str(
        result.stdout
    )


def kill():
    """
    说明:
        关闭ADB
    """
    global ADBOREDER, ADBPATH
    shell = [ADBPATH, "kill-server"]
    run(shell, shell=True, stdout=DEVNULL, check=False)


def input_swipe(pos1=(919, 617), pos2=(919, 908), time: int = 100):
    """
    说明:
        滑动屏幕
    参数:
        :param pos1: 坐标1
        :param pos2: 坐标2
        :param time: 操作时间(毫秒)
    """
    global ADBOREDER, ADBPATH
    shell = [
        ADBPATH,
        "-s",
        ADBOREDER,
        "shell",
        "input",
        "swipe",
        str(pos1[0] + random.randint(*EXCURSIONX)),
        str(pos1[1] + random.randint(*EXCURSIONY)),
        str(pos2[0] + random.randint(*EXCURSIONX)),
        str(pos2[1] + random.randint(*EXCURSIONY)),
        str(int(time)),
    ]
    run(shell, shell=True, check=False)


def input_tap(pos=(880, 362)):
    """
    说明:
        点击坐标
    参数:
        :param pos: 坐标
    """
    global ADBOREDER, ADBPATH
    shell = [
        ADBPATH,
        "-s",
        ADBOREDER,
        "shell",
        "input",
        "tap",
        str(pos[0] + random.randint(*EXCURSIONX)),
        str(pos[1] + random.randint(*EXCURSIONY)),
    ]
    run(shell, shell=True, check=False)


def screenshot() -> cv.typing.MatLike:
    """
    说明:
        截图
    参数:
        :param path: 手机中截图保存位置
    """
    global ADBOREDER, ADBPATH
    shell = [ADBPATH, "-s", ADBOREDER, "exec-out", "screencap", "-p"]
    result = run(shell, shell=True, capture_output=True, check=False)

    # 将截图数据转换为 NumPy 数组
    image_array = np.frombuffer(result.stdout, np.uint8)

    # 使用 OpenCV 解码图像数据
    screenshot = cv.imdecode(image_array, cv.IMREAD_COLOR)

    return screenshot
