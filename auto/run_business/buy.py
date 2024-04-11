"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:54:58
LastEditTime: 2024-04-11 23:02:46
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import List, Tuple

import cv2 as cv
import numpy as np
from loguru import logger

from core.adb import input_swipe, input_tap, screenshot
from core.exception_handling import get_excption
from core.image import crop_image, get_bgr, get_hsv
from core.ocr import predict
from core.presets import click, find_text, ocr_click


def buy_business(
    goods: List[str],
    num: int = 20,
    max_book: int = 0,
):
    """
    说明:
        购买商品
    参数:
        :param goods: 商品列表
        :param num: 期望议价的价格
        :param max_book: 最大使用进货书量
    """
    book = 0
    for good in goods:
        result, book = buy_good(good, book, max_book)
        if not result:
            logger.info(f"商品{good}购买失败")
        if (boatload := get_boatload()) == 0:
            logger.info("已满载")
            break
        logger.info(f"剩余载货量: {boatload}%")
    click_bargain_button(num)
    click_buy_button()
    time.sleep(0.5)
    return input_tap((896, 676))


def buy_good(good: str, book: int, max_book: int, again: bool = False):
    logger.info(f"正在购买: {good}")
    pos, image = find_text(
        good,
        cropped_pos1=(622, 136),
        cropped_pos2=(854, 685),
        log=False,
        return_image=True,
    )  # 点击商品
    if not pos:
        pos, image = find_good(good)  # 点击失败查找并点击商品
    if pos:
        hsv = get_hsv(image, pos)
        if hsv[-1] <= 80:
            if book < max_book:
                use_book(pos, book)
                return not again and buy_good(good, max_book, again=True)[0], book + 1
            else:
                return False, book
        else:
            click(pos)
            return True, book
    else:
        return False, book


def use_book(pos: Tuple[int, int], book: int):
    """
    说明:
        使用进货书
    """
    logger.info(f"使用进货书:{book}")
    click((pos[0] - 215, pos[1]))
    time.sleep(1.0)
    click((959, 541))
    while get_hsv(screenshot(), pos)[-1] < 80:
        time.sleep(0.5)


def find_good(good, timeout=10):
    """
    说明:
        查找并点击商品
    """
    start = time.time()
    while (spend_time := time.time() - start) < timeout:
        if spend_time < timeout / 2:
            input_swipe((678, 558), (693, 314))
        else:
            input_swipe((693, 314), (678, 558))
        # 等待拖到动画结束
        time.sleep(1)
        result, image = find_text(
            good,
            cropped_pos1=(622, 136),
            cropped_pos2=(854, 685),
            log=False,
            return_image=True,
        )
        if result:
            return result, image
    return None, None


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
