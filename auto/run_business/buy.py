"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:54:58
LastEditTime: 2024-04-05 21:49:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import List

import cv2 as cv
import numpy as np
from loguru import logger

from core.adb import input_swipe, input_tap, screenshot
from core.exception_handling import get_excption
from core.image import crop_image, get_bgr
from core.ocr import predict
from core.presets import ocr_click


def buy_business(goods: List[List[str]], num: int = 20):
    """
    说明:
        购买商品
    参数:
        :param goods: 商品列表
        :param num: 期望议价的价格
    """
    for item in goods:
        for good in item:
            logger.info(f"正在购买: {good}")
            result = ocr_click(
                good, cropped_pos1=(622, 136), cropped_pos2=(854, 685), log=False
            )  # 点击商品
            if not result:
                result = find_good(good)  # 点击失败查找并点击商品
            if (boatload := get_boatload()) == 0:
                logger.info("已满载")
                break
            logger.info(f"剩余载货量: {boatload}%")
    click_bargain_button(num)
    click_buy_button()
    time.sleep(0.5)
    return input_tap((896, 676))


def find_good(good, timeout=10):
    """
    说明:
        查找并点击商品
    """
    start = time.time()
    result = False
    while (spend_time := time.time() - start) < timeout:
        if spend_time < timeout / 2:
            input_swipe((678, 558), (693, 314))
        else:
            input_swipe((693, 314), (678, 558))
        # 等待拖到动画结束
        time.sleep(1)
        result = ocr_click(
            good, cropped_pos1=(622, 136), cropped_pos2=(854, 685), log=False
        )
        if result:
            return True
    return result


def get_boatload():
    """
    说明:
        获取载货量百分比
    """
    image = screenshot()
    lower_color_bound = np.array([36, 36, 36])
    upper_color_bound = np.array([36, 36, 36])

    y = 418
    x_start = 872
    x_end = 1240

    # 获取指定行的指定区间
    row_segment = image[y : y + 1, x_start:x_end]
    # 寻找指定颜色
    mask = cv.inRange(row_segment, lower_color_bound, upper_color_bound)

    boatload = np.sum(mask == 255) / (x_end - x_start)
    return int(boatload * 100)


def click_bargain_button(num=20):
    """
    说明:
        点击议价按钮
    参数:
        :param num: 期望议价的价格
    """
    for _ in range(5):
        reslut = predict(screenshot(), (993, 448), (1029, 477))
        if len(reslut) > 0:
            bargain = reslut[0]["text"]
            logger.info(f"降价幅度: {bargain}")
            if num == float(bargain[:-1]):
                return True
        if get_excption() == "议价次数不足":
            return False
        start = time.perf_counter()
        while time.perf_counter() - start < 5:
            bgr = get_bgr(screenshot(), (1176, 461))
            logger.debug(f"议价界面颜色检查: {bgr}")
            if [0, 130, 240] <= bgr <= [2, 133, 253]:
                input_tap((1177, 461))
                time.sleep(0.5)
            elif bgr == [251, 253, 253]:
                logger.info("议价次数不足")
                return True
    return False


def click_buy_button():
    """
    说明:
        点击购买按钮
    """
    start = time.time()
    while time.time() - start < 10:
        input_tap((1056, 647))
        time.sleep(1)
        image = screenshot()
        bgr = get_bgr(image, (1177, 459))
        logger.debug(f"购买物品界面颜色检查: {bgr}")
        if bgr != [2, 133, 253] and bgr != [251, 253, 253]:
            return True
    return False
