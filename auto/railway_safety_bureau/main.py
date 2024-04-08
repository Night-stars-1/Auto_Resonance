"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 19:51:16
LastEditTime: 2024-04-08 21:53:05
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.models.config import RSBModel, config
from core.presets import (
    click,
    click_image,
    click_station,
    find_text,
    go_outlets,
    wait,
    wait_fight_end,
    wait_time,
)

rsb = config.rsb


def join(city: str):
    click_station(city)
    go_outlets("铁安局")
    wait("railway_safety_bureau/railway_safety_bureau.png", (875, 27), (1093, 158), 10)
    click((903, 313))


def start():
    logger.info(f"开始铁安局 => {rsb.name}")
    join(rsb.city)

    wait("railway_safety_bureau/railway_safety_bureau.png", (174, 444), (294, 547), 10)
    click(rsb.levelSerialPos)
    while True:
        if not find_text(rsb.name) or rsb.name == "所有":
            click((87, 38))
            wait_time(1)
            click((932, 306))
        break
    click((883, 540))
    click_image("railway_safety_bureau/start_attack.png", (1133, 128), (1263, 628), 10)
    wait_fight_end()
    click((1154, 628))
    click((1154, 628))
