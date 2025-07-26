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
import numpy as np
from loguru import logger

from core.control.adb import ADB
from core.control.adb_port import EmulatorType
from core.control.base_control import IADB
from core.control.nemu import NEMU
from core.exception.exceptions import StopExecution
from core.image.image import Image
from core.model import app

EXCURSIONX = [-10, 10]
EXCURSIONY = [-10, 10]
STOP = False

control: IADB = ADB()


def connect(adb_port: Optional[int] = None):
    """
    连接ADB

    :param order: ADB端口
    """
    global control, STOP
    STOP = False
    device = app.Global.device
    if device.type == EmulatorType.MUMUV5:
        control = NEMU()
        status = control.connect(adb_port)
        if status:
            return status
        else:
            logger.warning("MUMUIPC连接失败，尝试使用ADB连接")
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
    pos_x1 = control.ratio * pos1[0] + random.randint(*EXCURSIONX)
    pos_y1 = control.ratio * pos1[1] + random.randint(*EXCURSIONY)
    pos_x2 = control.ratio * pos2[0] + random.randint(*EXCURSIONX)
    pos_y2 = control.ratio * pos2[1] + random.randint(*EXCURSIONY)

    logger.debug(f"滑动 ({pos_x1}, {pos_y1}) -> ({pos_x2}, {pos_y2})")
    while abs(pos_x2 - pos_x1) > 10 or abs(pos_y2 - pos_y1) > 10:
        limit_pos_x1 = max(20, min(pos_x1, control.safe_area[0]))
        limit_pos_y1 = max(70, min(pos_y1, control.safe_area[1]))
        limit_pos_x2 = max(20, min(pos_x2, control.safe_area[0]))
        limit_pos_y2 = max(70, min(pos_y2, control.safe_area[1]))
        logger.debug(
            f"多次滑动 ({limit_pos_x1}, {limit_pos_y1}) -> ({limit_pos_x2}, {limit_pos_y2})"
        )

        control.input_swipe(
            limit_pos_x1, limit_pos_y1, limit_pos_x2, limit_pos_y2, swipe_time
        )

        # 减去当前执行的距离
        pos_x1 -= limit_pos_x1 - limit_pos_x2
        pos_y1 -= limit_pos_y1 - limit_pos_y2


def input_tap(pos: Tuple[int, int] = (880, 362)):
    """
    点击坐标

    :param pos: 坐标
    """
    control.input_tap(
        int(control.ratio * pos[0] + random.randint(*EXCURSIONX)), int(control.ratio * pos[1] + random.randint(*EXCURSIONY))
    )


def screenshot() -> Image:
    """
    截图
    """
    if STOP:
        raise StopExecution()

    screenshot = screenshot_image()

    return Image(screenshot)


def screenshot_image() -> cv.typing.MatLike:
    """
    截图并返回图片对象
    """
    if STOP:
        raise StopExecution()

    screenshot = control.screenshot()
    screenshot = cv.resize(screenshot, control.dsize, interpolation=cv.INTER_AREA)
    return screenshot

def wait_stopped(threshold=7100000):
    """
    等待画面静止
    参数:
        :param threshold: 参数阈值
    """
    logger.info("等待图像静止")
    while True:
        gray1 = cv.cvtColor(screenshot_image(), cv.COLOR_BGR2GRAY)
        # 等待画面变动，并再次截图
        time.sleep(0.5)
        gray2 = cv.cvtColor(screenshot_image(), cv.COLOR_BGR2GRAY)

        # 计算两帧之间的绝对差异
        diff = cv.absdiff(gray1, gray2)

        # 计算差异值
        diff_sum: int = np.sum(diff)  # type: ignore
        logger.debug(f"画面差异 {diff_sum}")

        if diff_sum < threshold:
            break
        time.sleep(1)
