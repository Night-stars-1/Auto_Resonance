"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2025-02-11 16:56:45
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import platform
import random
import time
from subprocess import DEVNULL, CompletedProcess
from subprocess import run as _run
from typing import Tuple

import cv2 as cv
import numpy as np
from loguru import logger

from core.adb.adb_port import get_adb_port
from core.model import app

from ..exceptions import StopExecution

ADBOREDER = ""
ADBPATH = ""
EXCURSIONX = [-10, 10]
EXCURSIONY = [-10, 10]
STOP = False


def run(
    *popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs
) -> CompletedProcess:
    return _run(
        *popenargs,
        shell=True if platform.system() == "Windows" else False,
        input=input,
        capture_output=capture_output,
        timeout=timeout,
        check=check,
        **kwargs,
    )


def connect(adb_port: int = 0, name="自定义"):
    """
    说明:
        连接ADB
    参数:
        :param order: ADB端口
    """
    global ADBOREDER, ADBPATH, STOP
    if adb_port == 0:
        adb_port, name = get_adb_port()
    if adb_port is None:
        logger.info("未知ADB端口信息")
        return False
    logger.info(f"ADB端口： {adb_port} 来自: {name}")
    ADBOREDER = f"127.0.0.1:{adb_port}"
    ADBPATH = app.Global.adbPath
    STOP = False
    shell = [ADBPATH, "connect", ADBOREDER]
    result = run(shell, capture_output=True, check=False)
    status = "already connected" in str(result.stdout) or "connected to" in str(
        result.stdout
    )
    if not status:
        logger.error(f"连接失败: {result.stdout.decode()}")
    return status and STOP


def stop():
    global STOP
    STOP = True


def kill():
    """
    说明:
        关闭ADB
    """
    global ADBOREDER, ADBPATH
    shell = [ADBPATH, "kill-server"]
    run(shell, stdout=DEVNULL, check=False)


def input_swipe(pos1=(919, 617), pos2=(919, 908), swipe_time: int = 100):
    """
    说明:
        滑动屏幕(可超出屏幕)
    参数:
        :param pos1: 坐标1
        :param pos2: 坐标2
        :param time: 操作时间(毫秒)
    """
    global ADBOREDER, ADBPATH
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

        shell = [
            ADBPATH,
            "-s",
            ADBOREDER,
            "shell",
            "input",
            "swipe",
            str(limit_pos_x1),
            str(limit_pos_y1),
            str(limit_pos_x2),
            str(limit_pos_y2),
            str(int(swipe_time)),
        ]
        run(shell, check=False)
        time.sleep(swipe_time / 1000)
        # 减去当前执行的距离
        pos_x1 -= limit_pos_x1 - limit_pos_x2
        pos_y1 -= limit_pos_y1 - limit_pos_y2
        # pos_x2 -= limit_pos_x2
        # pos_y2 -= limit_pos_y2


def input_tap(pos: Tuple[int, int] = (880, 362)):
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
    run(shell, check=False)


def screenshot() -> cv.typing.MatLike:
    """
    截图
    """
    global ADBOREDER, ADBPATH, STOP
    if STOP:
        raise StopExecution()
    shell = [ADBPATH, "-s", ADBOREDER, "exec-out", "screencap", "-p"]
    result = run(shell, capture_output=True, check=False)

    # 将截图数据转换为 NumPy 数组
    image_array = np.frombuffer(result.stdout, np.uint8)

    screenshot = cv.imdecode(image_array, cv.IMREAD_COLOR)

    return screenshot
