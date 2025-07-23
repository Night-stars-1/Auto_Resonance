"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2025-02-11 16:56:45
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import random
import time
from typing import Optional, Tuple

import cv2 as cv
from loguru import logger

from core.adb.adb import ADB
from core.adb.base_control import IADB
from core.model import app

from ..exceptions import StopExecution

EXCURSIONX = [-10, 10]
EXCURSIONY = [-10, 10]
STOP = False

control: IADB = ADB()


def connect(adb_port: Optional[int] = None):
    """
    连接ADB

    :param order: ADB端口
    """
    global control
    control = ADB()

    status = control.connect(adb_port)
    return status


def stop():
    global STOP
    STOP = True


def kill():
    """
    关闭连接
    """
    control.kill()


def input_swipe(pos1=(919, 617), pos2=(919, 908), swipe_time: int = 100):
    """
    滑动屏幕(可超出屏幕)

    :param pos1: 坐标1
    :param pos2: 坐标2
    :param time: 操作时间(毫秒)
    """
    # 添加随机值
    pos_x1 = pos1[0] + random.randint(*EXCURSIONX)
    pos_y1 = pos1[1] + random.randint(*EXCURSIONY)
    pos_x2 = pos2[0] + random.randint(*EXCURSIONX)
    pos_y2 = pos2[1] + random.randint(*EXCURSIONY)

    logger.debug(f"滑动 ({pos_x1}, {pos_y1}) -> ({pos_x2}, {pos_y2})")
    while abs(pos_x2 - pos_x1) > 10 or abs(pos_y2 - pos_y1) > 10:
        limit_pos_x1 = max(20, min(pos_x1, 1200))
        limit_pos_y1 = max(70, min(pos_y1, 700))
        limit_pos_x2 = max(20, min(pos_x2, 1200))
        limit_pos_y2 = max(70, min(pos_y2, 700))
        logger.debug(
            f"多次滑动 ({limit_pos_x1}, {limit_pos_y1}) -> ({limit_pos_x2}, {limit_pos_y2})"
        )

        control.input_swipe(
            limit_pos_x1, limit_pos_y1, limit_pos_x2, limit_pos_y2, swipe_time
        )

        time.sleep(swipe_time / 1000)
        # 减去当前执行的距离
        pos_x1 -= limit_pos_x1 - limit_pos_x2
        pos_y1 -= limit_pos_y1 - limit_pos_y2


def input_tap(pos: Tuple[int, int] = (880, 362)):
    """
    点击坐标

    :param pos: 坐标
    """
    control.input_tap(
        pos[0] + random.randint(*EXCURSIONX), pos[1] + random.randint(*EXCURSIONY)
    )


def screenshot() -> cv.typing.MatLike:
    """
    截图
    """
    if STOP:
        raise StopExecution()

    screenshot = control.screenshot()

    return screenshot
