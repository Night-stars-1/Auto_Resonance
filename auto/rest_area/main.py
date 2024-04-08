"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 19:51:16
LastEditTime: 2024-04-08 20:46:40
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger

from core.models.config import RSBModel
from core.presets import click, find_text, go_home, go_outlets, wait, wait_time


def join():
    go_home()
    go_outlets("休息区")
    wait("rest_area/rest_area_logo.png", (918, 48), (1049, 153), 10)


def start():
    logger.info(f"开始银枝气泡水")
    join()

    wait("rest_area/rest_area_logo.png", (918, 48), (1049, 153), 10)
    click((937, 407))
    wait("rest_area/heiyue_rest_area.png", (594, 58), (692, 140), 10)
    if find_text("桦石"):
        click((967, 539))
        wait_time(1.5)
        click((530, 700))
    go_home()
