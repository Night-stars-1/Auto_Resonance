"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:54:58
LastEditTime: 2025-02-11 19:29:24
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import List, Tuple

import cv2 as cv
import numpy as np
from loguru import logger

from core.control.control import input_swipe, input_tap, screenshot, screenshot_image
from core.exception.exception_handling import get_excption
from core.image.image import Image
from core.module.bgr import BGR
from core.module.hsv import HSV
from core.preset import click, find_text, go_home
from core.preset.control import wait_gbr


def buy_business(
    primary_goods: List[str],
    secondary_goods: List[str],
    num: int = 0,
    max_book: int = 0,
):
    """
    购买商品

    :param primary_goods: 主要商品列表
    :param secondary_goods: 次要商品列表
    :param num: 议价的次数
    :param max_book: 最大使用进货书量
    """

    def process_goods(book, good):
        if (boatload := get_boatload()) == 0:
            logger.info("已满载")
            return True
        result, book = buy_good(good, book, max_book)
        if result is None:
            logger.info(f"进货书已用完")
        elif not result:
            logger.info(f"商品{good}购买失败")
        logger.info(f"剩余载货量: {boatload}%")
        return book

    book = 0
    done = False
    for i in range(max_book + 1):
        if done:
            break
        for good in primary_goods:
            if (book := process_goods(book, good)) is True:
                done = True
                break
    for good in secondary_goods:
        if (book := process_goods(book, good)) is True:
            break
    if not is_empty_goods():
        click_bargain_button(num)
        click_buy_button()
        time.sleep(0.5)
        return input_tap((896, 676))
    else:
        logger.error("未购买物品")
        go_home()


def is_empty_goods():
    image = screenshot()
    image.crop_image((870, 132), (994, 205))
    bgr = image.get_bgr((898, 169))
    logger.debug(f"货物是否为空检查 {bgr}")
    return BGR(27, 26, 26) == bgr


def buy_good(good: str, book: int, max_book: int, again: bool = False):
    logger.info(f"正在购买: {good}")
    pos, image = find_text(
        good,
        cropped_pos1=(622, 136),
        cropped_pos2=(854, 685),
        log=False,
    )  # 点击商品
    if not pos:
        pos, image = find_good(good)  # 点击失败查找并点击商品
    if pos and image is not None:
        bgr = image.get_bgr((641, pos[1]))
        logger.debug(f"是否进货检测: {bgr}")
        if 13 <= bgr.r <= 16:
            if book < max_book:
                use_book(pos, book)
                return (
                    not again and buy_good(good, book, max_book, again=True)[0],
                    book + 1,
                )  # 如果不是重复运行则使用再次购买，进货书使用次数+1
            else:
                return None, book
        else:
            logger.info(f"点击商品: {good}")
            click(pos)
            return True, book
    else:
        return False, book


def use_book(pos: Tuple[int, int], book: int):
    """
    说明:
        使用进货书
    """
    logger.info(f"使用进货书:{book+1}")
    click((pos[0] - 215, pos[1]))
    time.sleep(1.0)
    click((959, 541))
    while (hsv := screenshot().get_hsv(pos))[-1] < 60:
        logger.debug(f"进货书是否所有成功颜色检查: {hsv}")
        time.sleep(0.5)


def find_good(good, timeout=10):
    """
    说明:
        查找并点击商品
    """
    start = time.time()
    while (spend_time := time.time() - start) < timeout:
        if spend_time < timeout / 2:
            input_swipe((678, 558), (693, 314), swipe_time=500)
        else:
            input_swipe((693, 314), (678, 558), swipe_time=500)
        # 等待拖到动画结束
        time.sleep(1)
        result, image = find_text(
            good,
            cropped_pos1=(622, 136),
            cropped_pos2=(854, 685),
            log=False,
        )
        if result:
            return result, image
    return None, None


def get_boatload():
    """
    说明:
        获取载货量百分比
    """
    image = screenshot_image()
    lower_color_bound = np.array([35, 35, 35])
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


def click_bargain_button_of_bargain(target_bargain=0):
    """
    说明:
        点击议价按钮
    参数:
        :param target_bargain: 目标议价百分比
    """
    start = time.perf_counter()
    while time.perf_counter() - start < 15:
        image = screenshot()
        image.crop_image((988, 450), (1042, 475))
        reslut = image.ocr()
        bargain = reslut[0]["text"][:-1] if len(reslut) > 0 else None
        logger.info(f"降价幅度: {bargain}%")
        if bargain and target_bargain <= bargain:
            return True
        if get_excption() == "议价次数不足":
            return False
        bgr = screenshot().get_bgr((1176, 461))
        logger.debug(f"降价界面颜色检查: {bgr}")
        if BGR(5, 135, 245) == bgr:
            input_tap((1177, 461))
            time.sleep(0.5)
        elif bgr == [251, 253, 253]:
            logger.info("议价次数不足")
            return True
        elif bgr == [62, 63, 63]:
            logger.info("疲劳不足")
            input_tap((83, 36))
            return True
    return False


def click_bargain_button(num=0):
    """
    说明:
        点击议价按钮
    参数:
        :param num: 议价次数
    """
    logger.info(f"议价次数: {num}")
    start = time.perf_counter()
    while time.perf_counter() - start < 15:
        if num <= 0:
            return True
        bgr = screenshot().get_bgr((1176, 461))
        logger.debug(f"降价界面颜色检查: {bgr}")
        if BGR(0, 123, 240) <= bgr <= BGR(2, 133, 255):
            input_tap((1177, 461))
            time.sleep(1.0)
        elif bgr == [251, 253, 253]:
            logger.info("降价次数不足")
            return True
        elif bgr == [62, 63, 63]:
            logger.info("疲劳不足")
            input_tap((83, 36))
            return True
        hsv = screenshot().crop_image((516, 224), (787, 439)).get_hsv((629, 271))
        logger.debug(f"降价是否成功颜色检查(HSV): {hsv}")
        if 95 <= hsv.h <= 105:
            logger.info("降价成功")
            num -= 1
        else:
            logger.info("降价失败")
        # 等待降价动画消失
        wait_gbr((628, 102), BGR(60, 55, 30), BGR(70, 65, 40))
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
        bgr = image.get_bgr((1177, 459), offset=5)
        logger.debug(f"购买物品界面颜色检查: {bgr}")
        if bgr != [2, 133, 253] and bgr != [251, 253, 253]:
            return True
    return False
