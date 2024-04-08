"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:24:47
LastEditTime: 2024-04-08 13:26:02
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core import ocr

from ..adb import input_swipe, input_tap, screenshot
from ..image import get_all_color_pos, get_bgrs, match_screenshot
from ..ocr import predict
from ..presets import blurry_ocr_click, wait
from .control import click_image
from .station import STATION

FIGHT_TIME = 1000

STATION_NAME2PNG = {
    "7号自由港": "qhzyg.png",
    "澄明数据中心": "cmsjzx.png",
    "阿妮塔战备工厂": "antzb.png",
    "阿妮塔能源研究所": "antnyjjs.png",
    "淘金乐园": "tjly.png",
    "曼德矿场": "mdkc.png",
    "荒原站": "hyz.png",
    "铁盟哨站": "tmsz.png",
    "修格里城": "xglc.png",
}


def click_station(name: str):
    logger.info(f"点击站点 => {name}")
    if match_screenshot(screenshot(), "resources/main_map.png")["max_val"] < 0.95:
        logger.info("未检测到主地图界面，返回主地图")
        go_home()
    reslut = predict(screenshot(), cropped_pos1=(1131, 498), cropped_pos2=(1226, 515))
    if name in [item["text"] for item in reslut]:
        logger.info("已在目标站点")
        return True
    logger.info("检测到主地图界面，点击地图")
    input_tap((1201, 666))
    time.sleep(1)

    def select_station(name):
        n = 0
        for _ in range(6):
            logger.info(f"尝试点击站点 => {n}")
            result = match_screenshot(
                screenshot(), f"resources/stations/{STATION_NAME2PNG[name]}"
            )
            if result["max_val"] > 0.95:
                input_tap(result["max_loc"])
                break
            if 0 <= n <= 1:
                input_swipe((599, 656), (600, 129), time=500)
                time.sleep(0.5)
            elif n == 2:
                input_swipe((999, 388), (191, 367), time=500)
                time.sleep(0.5)
            elif 3 <= n <= 5:
                input_swipe((600, 129), (599, 656), time=500)
                time.sleep(0.5)
            else:
                input_swipe((191, 367), (999, 388), time=500)
                time.sleep(0.5)
            n += 1

    select_station(name)
    time.sleep(0.5)
    # 点击前往目的地按钮
    logger.info("点击前往目的地按钮")
    for _ in range(3):
        if click_image(
            "resources/map/go_station.png",
            cropped_pos1=(937, 605),
            cropped_pos2=(1218, 679),
        ):
            return STATION(True)
        time.sleep(0.5)
    return click_station_ocr(name)


def click_station_ocr(name: str):
    """
    说明:
        OCR点击指定站点
    参数:
        :param name: 站点名称
    """
    logger.info(f"通过OCR识别站点 => {name}")
    if match_screenshot(screenshot(), "resources/main_map.png")["max_val"] > 0.95:
        logger.info("检测到主地图界面，点击地图")
        input_tap((1201, 666))
        time.sleep(1)

    def select_station(name):
        n = 0
        for _ in range(6):
            logger.info(f"尝试点击站点 => {n}")
            all_pos = get_all_color_pos(screenshot())
            for pos in all_pos:
                input_tap(pos)
                time.sleep(0.5)
                data = predict(
                    screenshot(), cropped_pos1=(764, 100), cropped_pos2=(1070, 132)
                )
                logger.info([item["text"] for item in data])
                for item in data:
                    if item["text"] == name:
                        return
                    else:
                        input_tap((86, 415))
                        time.sleep(1.5)
            if 0 <= n <= 1:
                input_swipe((599, 656), (600, 129), time=500)
                time.sleep(0.5)
            elif n == 2:
                input_swipe((999, 388), (191, 367), time=500)
                time.sleep(0.5)
            elif 3 <= n <= 5:
                input_swipe((600, 129), (599, 656), time=500)
                time.sleep(0.5)
            else:
                input_swipe((191, 367), (999, 388), time=500)
                time.sleep(0.5)
            n += 1

    select_station(name)
    time.sleep(0.5)
    # 点击前往目的地按钮
    logger.info("点击前往目的地按钮")
    for _ in range(3):
        if click_image(
            "resources/map/go_station.png",
            cropped_pos1=(937, 605),
            cropped_pos2=(1218, 679),
        ):
            return STATION(True)
        time.sleep(0.5)
    return STATION(False)


def go_city():
    """
    说明:
        进入城市界面
    """
    input_tap((1174, 494))
    wait("resources/fame.png", cropped_pos1=[25, 634], cropped_pos2=[99, 707])


def go_outlets(name: str):
    """
    说明:
        前往指定门店
    参数:
        :param name: 门店名称
    """
    go_city()
    logger.info(f"前往 => {name}")
    if result := blurry_ocr_click(name, excursion_pos=(-2, 30), log=False):
        return result
    input_swipe((969, 369), (457, 340), time=500)
    if result := blurry_ocr_click(name, excursion_pos=(-2, 30), log=False):
        return result
    input_swipe((641, 246), (637, 615), time=500)
    if result := blurry_ocr_click(name, excursion_pos=(-2, 30)):
        return result


def go_home():
    """
    说明:
        返回主界面
    """
    logger.info("返回主界面")

    def wait_home():
        time.sleep(1)
        while (
            match_screenshot(screenshot(), "resources/main_map.png")["max_val"] < 0.95
        ):
            time.sleep(1)

    input_tap((228, 27))
    wait_home()


def wait_fight_end():
    """
    说明:
        等待战斗结束
    """
    logger.info("等待战斗结束")
    start = time.perf_counter()
    while time.perf_counter() - start < FIGHT_TIME:
        bgrs = get_bgrs(screenshot(), [(1114, 630), (1204, 624), (236, 26)])
        if [245, 245, 245] <= bgrs[0] <= [255, 255, 255] and [0, 0, 0] <= bgrs[1] <= [
            10,
            10,
            10,
        ]:
            logger.info("战斗结束")
            input_tap((1151, 626))
            return True
        elif bgrs[2] == [124, 126, 125]:
            logger.info("开启自动战斗")
            input_tap((233, 44))
        time.sleep(3)
    logger.error("战斗超时")
    return False
