"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 15:17:19
LastEditTime: 2024-04-21 17:23:19
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.adb import input_tap, screenshot
from core.exception_handling import get_excption
from core.image import get_bgr
from core.ocr import predict
from core.utils import compare_ranges


def sell_business(num=20):
    """
    说明:
        出售所有商品
    参数:
        :param num: 期望议价的价格
    """
    logger.info("出售全部货物")
    time.sleep(0.5)
    input_tap((1187, 103))
    time.sleep(0.5)
    if is_empty_goods():
        logger.error("检测到未成功出售物品")
        return False
    else:
        click_bargain_button(num)
        click_sell_button()
        time.sleep(0.5)
        return input_tap((896, 676))


def is_empty_goods():
    bgr = get_bgr(
        screenshot(), (898, 169), cropped_pos1=(870, 132), cropped_pos2=(994, 205)
    )
    return compare_ranges([22, 27, 27], bgr, [22, 27, 27])


def click_bargain_button(num=20):
    start = time.perf_counter()
    while time.perf_counter() - start < 15:
        reslut = predict(screenshot(), (993, 448), (1029, 477))
        bargain = reslut[0]["text"][:-1] if len(reslut) > 0 else None
        logger.info(f"抬价幅度: {bargain}%")
        if bargain and num <= float(bargain):
            return True
        if get_excption() == "议价次数不足":
            return False
        bgr = get_bgr(screenshot(), (1176, 461))
        logger.debug(f"抬价界面颜色检查: {bgr}")
        if compare_ranges([0, 170, 240], bgr, [0, 183, 253]):
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


def click_sell_button():
    start = time.time()
    while time.time() - start < 10:
        input_tap((1056, 647))
        time.sleep(1)
        image = screenshot()
        bgr = get_bgr(image, (1175, 470))
        logger.debug(f"出售物品界面颜色检查: {bgr}")
        if bgr == [227, 131, 82]:
            logger.info("检测到包含本地商品")
            input_tap((975, 498))
        if bgr != [0, 183, 253] and bgr != [227, 131, 82] and bgr != [251, 253, 253]:
            return True
    return False
