"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 18:06:25
LastEditTime: 2024-04-19 14:57:32
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Tuple

from loguru import logger

from core.module.bgr import BGRGroup

from ..adb import input_tap, screenshot
from ..exception_handling import get_excption
from ..image import get_bgr, match_screenshot
from ..ocr import predict
from .decorator import ensure_resources_prefix


@ensure_resources_prefix
def wait(
    image: str,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    trynum=10,
    threshold=0.95,
):
    """
    说明:
        等待指定图片出现
    参数:
        :param image: 图片路径
        :param cropped_pos: 裁剪坐标
        :param trynum: 尝试次数
        :param threshold: 阈值
    """
    for _ in range(trynum):
        result = match_screenshot(screenshot(), image, cropped_pos1, cropped_pos2)
        if result["max_val"] >= threshold:
            return True
        time.sleep(1)
    logger.info(get_excption())
    return False


def wait_gbr(
    pos: Tuple[int, int],
    min_gbr: Tuple[int, int, int],
    max_gbr: Tuple[int, int, int],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    trynum=10,
):
    """
    说明:
        等待指定图片出现
    参数:
        :param pos: 坐标
        :param min_gbr: 最小颜色
        :param max_gbr: 最大颜色
        :param cropped_pos1: 裁剪坐标
        :param cropped_pos2: 裁剪坐标
        :param trynum: 尝试次数
    """
    for _ in range(trynum):
        bgr = get_bgr(screenshot(), pos, cropped_pos1, cropped_pos2)
        if BGRGroup(min_gbr, max_gbr) == bgr:
            return True
        time.sleep(1)
    logger.info(get_excption())
    return False


def wait_time(seconds: float):
    """
    说明:
        等待指定时间
    参数:
        :param time: 时间
    """
    time.sleep(seconds)


@ensure_resources_prefix
def click_image(
    image: str,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    excursion_pos: Tuple[int, int] = (0, 0),
    trynum=10,
):
    """
    说明:
        点击指定图片
    参数:
        :param image_path: 图片路径
        :param cropped_pos1: 裁剪坐标1
        :param cropped_pos2: 裁剪坐标2
        :param excursion_pos: 点击偏移坐标
        :param trynum: 尝试次数
    """
    time.sleep(0.5)
    for _ in range(trynum):
        result = match_screenshot(screenshot(), image, cropped_pos1, cropped_pos2)
        if result["max_val"] > 0.95:
            pos = (
                result["max_loc"][0] + excursion_pos[0],
                result["max_loc"][1] + excursion_pos[1],
            )
            input_tap(pos)
            return True
    logger.error(f"未找到指定图片 => {image}")
    logger.info(get_excption())
    return False


def click(pos):
    """
    说明:
        点击指定坐标
    参数:
        :param pos: 坐标
    """
    input_tap(pos)


def ocr_click(
    text: str,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    log=True,
):
    """
    说明:
        点击指定文本
    参数:
        :param text: 文本
        :param cropped_pos1: 裁剪坐标1
        :param cropped_pos2: 裁剪坐标2
        :param log: 是否打印日志
    """
    image = screenshot()
    data = predict(image, cropped_pos1, cropped_pos2)
    coordinates = None
    for item in data:
        if item["text"] == text:
            position = item["position"]
            # 计算中心坐标
            center_x = (position[0][0] + position[2][0]) / 2
            center_y = (position[0][1] + position[2][1]) / 2
            coordinates = (center_x, center_y)
            break
    if coordinates:
        input_tap(coordinates)
        return True
    else:
        if log:
            logger.error(f"未找到指定文本 => {text}")
        return False


def blurry_ocr_click(
    text: str,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    excursion_pos: Tuple[int, int] = (0, 0),
    trynum=3,
    log=True,
):
    """
    说明:
        模糊点击文本
    参数:
        :param text: 文本
        :param cropped_pos1: 裁剪坐标1
        :param cropped_pos2: 裁剪坐标2
        :param excursion_pos: 点击偏移坐标
        :param trynum: 尝试次数
    """
    for _ in range(trynum):
        image = screenshot()
        data = predict(image, cropped_pos1, cropped_pos2)
        coordinates = None
        for item in data:
            if text in item["text"]:
                # 读取位置信息
                position = item["position"]
                # 计算中心坐标
                center_x = (position[0][0] + position[2][0]) / 2
                center_y = (position[0][1] + position[2][1]) / 2
                coordinates = (center_x + excursion_pos[0], center_y + excursion_pos[1])
                break
        if coordinates:
            input_tap(coordinates)
            return True
    if log:
        logger.error(f"未找到指定文本 => {text}")
    return False


def find_text(
    text: str,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    log=True,
    return_image=False,
):
    """
    说明:
        查找文本
    参数:
        :param text: 文本
        :param cropped_pos1: 裁剪坐标1
        :param cropped_pos2: 裁剪坐标2
        :param image: 是否返回图片
    """
    image = screenshot()
    data = predict(image, cropped_pos1, cropped_pos2)
    for item in data:
        if text in item["text"]:
            if log:
                logger.info(f"找到文本 => {text}")
            position = item["position"]
            # 计算中心坐标
            center_x = (position[0][0] + position[2][0]) / 2
            center_y = (position[0][1] + position[2][1]) / 2
            if return_image:
                return (center_x, center_y), image
            return (center_x, center_y)
    if log:
        logger.error(f"未找到指定文本 => {text}")
    if return_image:
        return None, None
    return None
