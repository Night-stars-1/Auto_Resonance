"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-25 23:12:06
LastEditTime: 2024-04-29 20:55:11
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Tuple

from loguru import logger

from core.adb import connect, input_tap, screenshot
from core.image import get_bgr
from core.module.bgr import BGR, BGRGroup
from core.presets import click_station, go_home, go_outlets

from ..run_business import buy_business, go_business


def go_assistance_center():
    go_home()
    go_outlets("工程援助中心")
    while BGR(251, 126, 65) != (
        bgr := get_bgr(
            screenshot(), (300, 669), cropped_pos1=(289, 640), cropped_pos2=(424, 701)
        )
    ):
        logger.debug(f"是否进入工程援助中心颜色检查: {bgr}")
        time.sleep(0.5)
    input_tap((844, 408))
    time.sleep(0.5)


def get_consign_pos():
    """
    说明:
        获取交付按钮坐标
    """
    # 监测联盟币 联盟币是否交付 其他资源是否交付
    bgr = get_bgr(
        screenshot(), (541, 366), cropped_pos1=(483, 317), cropped_pos2=(630, 418)
    )
    if BGRGroup([0, 90, 115], [1, 100, 125]) == bgr:
        logger.info("联盟币未交付")
        return (710, 662)
    else:
        logger.info("联盟币已交付")
        return (454, 663)


def consign_goods(pos: Tuple[int, int]):
    """
    说明:
        交付货物
    参数:
        :param pos: 交付按钮坐标
    """
    logger.info("开始交付物质")
    while BGRGroup([0, 170, 240], [1, 182, 250]) == get_bgr(
        screenshot(), pos, cropped_pos1=(431, 637), cropped_pos2=(924, 694)
    ):
        input_tap(pos)
        time.sleep(1.0)
        input_tap((797, 500))
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < 10:
            bgr = get_bgr(
                screenshot(), (66, 301), cropped_pos1=(19, 266), cropped_pos2=(85, 315)
            )
            if BGRGroup([6, 6, 6], [8, 8, 8]) == bgr:
                input_tap((91, 109))
                break
    logger.info("交付完成")


def transport_order(num: int = 1):
    status = connect()
    if not status:
        logger.error("ADB连接失败")
        return False
    for n in range(num):
        logger.info(f"开始运输订单 => {n+1}")
        go_assistance_center()
        pos = get_consign_pos()
        check_consign_gbr = get_bgr(
            screenshot(), pos, cropped_pos1=(431, 637), cropped_pos2=(924, 694)
        )
        is_consign = BGRGroup([0, 170, 240], [1, 182, 250]) == check_consign_gbr
        logger.debug(f"交付坐标: {pos} {check_consign_gbr} {is_consign}")
        if not is_consign:
            go_home()
            click_station("曼德矿场").wait()
            go_business("buy")
            buy_business(
                [],
                ["砂石", "石材", "建材", "钢筋混凝土轨枕", "轨枕用特种钢材", "铁矿石"],
                num=0,
                max_book=0,
            )
            go_home()
            click_station("7号自由港").wait()
            go_assistance_center()
            consign_goods((710, 662))
        else:
            consign_goods(pos)
