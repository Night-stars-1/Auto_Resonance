"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 19:51:16
LastEditTime: 2024-05-11 00:35:10
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from datetime import datetime

from loguru import logger

from core.models.config import config
from core.presets import (
    click,
    get_city,
    go_home,
    go_outlets,
    ocr_click,
    wait,
    wait_time,
)


def join():
    go_home()
    go_outlets("休息区")
    wait("rest_area/rest_area_logo.png", (918, 48), (1049, 153), 10)


def start():
    logger.info(f"开始购买桦石")
    if time.time() - config.rest_area.huashi.runtime > 86400:
        city = get_city()
        if city in [
            "七号自由港",
            "澄明数据中心",
            "曼德矿场",
            "修格里城",
            "阿妮塔发射中心",
        ]:
            join()

            wait("rest_area/rest_area_logo.png", (918, 48), (1049, 153), 10)
            click((937, 407))
            wait("rest_area/heiyue_rest_area.png", (594, 58), (692, 140), 10)
            if ocr_click("桦石"):
                wait_time(1.0)
                click((990, 537))
                wait_time(1.5)
                click((458, 682))
                config.rest_area.huashi.runtime = time.time()
            go_home()
        else:
            logger.info(f"当前站点: {city} 无休息区")
    else:
        logger.info(
            f"今天已购买桦石，购买时间: {datetime.fromtimestamp(config.rest_area.huashi.runtime).strftime('%Y-%m-%d %H:%M:%S')}"
        )
