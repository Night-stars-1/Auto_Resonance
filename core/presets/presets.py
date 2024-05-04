"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:24:47
LastEditTime: 2024-05-04 15:32:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.module.bgr import BGRGroup

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
    "阿妮塔战备工厂": "antzbgc.png",
    "阿妮塔能源研究所": "antnyyjs.png",
    "阿妮塔发射中心": "antfszx.png",
    "淘金乐园": "tjly.png",
    "曼德矿场": "mdkc.png",
    "荒原站": "hyz.png",
    "铁盟哨站": "tmsz.png",
    "修格里城": "xglc.png",
}

STATION_POS_DATA = {
    "澄明数据中心": (1049, 345),
    "7号自由港": (665, 577),
    "阿妮塔战备工厂": (832, 664),
    "阿妮塔发射中心": (164, 420 + 577),
    "阿妮塔能源研究所": (614, 454 + 577),
    "修格里城": (285 + 1049, 121 + 345),
    "铁盟哨站": (501 + 1049, 122 + 345),
    "荒原站": (753 + 1049, 121 + 345),
    "曼德矿场": (602 + 1049, 322 + 345),
    "淘金乐园": (701 + 1049, 604 + 345),
}


def calculate_station_differences(station_map_data: dict):
    differences = {}
    for site1, coords1 in station_map_data.items():
        for site2, coords2 in station_map_data.items():
            if site1 != site2:
                x_diff = coords2[0] - coords1[0]
                y_diff = coords2[1] - coords1[1]
                differences[(site1, site2)] = (x_diff, y_diff)
    return differences


# 计算站点之间的差值
STATION_DIFFERENCES = calculate_station_differences(STATION_POS_DATA)


def click_station(name: str):
    """
    说明:
        点击站点
    参数:
        :param name: 目标站点
    """
    source = ""
    logger.info(f"点击站点 => {name}")
    if match_screenshot(screenshot(), "resources/main_map.png")["max_val"] < 0.95:
        logger.info("未检测到主地图界面，返回主地图")
        go_home()
    reslut = predict(screenshot(), cropped_pos1=(1131, 498), cropped_pos2=(1238, 516))
    if len(reslut) > 0:
        source = reslut[0]["text"]
        logger.info(f"当前站点: {source}")
        if name in [item["text"] for item in reslut]:
            logger.info("已在目标站点")
            return STATION(True, is_destine=True)
    logger.info("检测到主地图界面，点击地图")
    input_tap((1201, 666))
    time.sleep(1)

    city_differences = STATION_DIFFERENCES.get((source, name))
    if city_differences:
        source_x = 640
        source_y = 360
        # 如果有路线则进行寻找
        x1 = source_x + city_differences[0]
        if (x_distance := x1 - 1280) > 0:
            x1 = 1280
            source_x = source_x - x_distance
        elif (x_distance := x1 - 0) < 0:
            x1 = 0
            source_x = source_x - x_distance
        y1 = source_y + city_differences[1]
        if (y_distance := y1 - 720) > 0:
            y1 = 720
            source_y = source_y - y_distance
        elif (y_distance := y1 - 78) < 0:
            y1 = 78
            source_y = source_y - y_distance

        # 滑动到目标站点
        input_swipe((x1, y1), (source_x, source_y), time=500)

        result = match_screenshot(
            screenshot(), f"resources/stations/{STATION_NAME2PNG[name]}"
        )
        if result["max_val"] > 0.95:
            # 点击站点
            input_tap(result["max_loc"])
        time.sleep(0.5)
        # 点击前往目的地按钮
        logger.info("点击前往目的地按钮")
        if click_image(
            "resources/map/go_station.png",
            cropped_pos1=(937, 605),
            cropped_pos2=(1218, 679),
            trynum=5,
        ):
            return STATION(True)
    return multiple_slide_click_station(name)


def multiple_slide_click_station(name: str):
    """
    说明:
        多次滑动点击站点
    参数:
        :param name: 站点名称
    """
    logger.info(f"多次滑动点击站点 => {name}")
    if match_screenshot(screenshot(), "resources/main_map.png")["max_val"] > 0.95:
        logger.info("检测到主地图界面，点击地图")
        input_tap((1201, 666))
        time.sleep(1)

    if match_screenshot(screenshot(), "resources/main_map.png")["max_val"] > 0.95:
        logger.info("检测到主地图界面，点击地图")
        input_tap((1201, 666))
        time.sleep(1)

    def select_station(name):
        n = 0
        for _ in range(12):
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
            elif 6 <= n <= 9:
                input_swipe((191, 367), (999, 388), time=500)
                time.sleep(0.5)
            else:
                input_swipe((599, 656), (600, 129), time=500)
                time.sleep(0.5)
            n += 1

    select_station(name)
    time.sleep(0.5)
    # 点击前往目的地按钮
    logger.info("点击前往目的地按钮")
    if click_image(
        "resources/map/go_station.png",
        cropped_pos1=(937, 605),
        cropped_pos2=(1218, 679),
        trynum=5,
    ):
        return STATION(True)
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
        for _ in range(10):
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
            elif 6 <= n <= 8:
                input_swipe((191, 367), (999, 388), time=500)
                time.sleep(0.5)
            else:
                input_swipe((599, 656), (600, 129), time=500)
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


def get_city():
    """
    说明:
        获取当前城市
    """
    go_home()
    reslut = predict(screenshot(), cropped_pos1=(1131, 498), cropped_pos2=(1238, 516))
    logger.info(f"当前站点: {reslut[0]['text']}")
    return reslut[0]["text"]


def go_city():
    """
    说明:
        进入城市界面
    """
    while (
        match_screenshot(
            screenshot(),
            "resources/fame.png",
            cropped_pos1=[25, 634],
            cropped_pos2=[99, 707],
        )["max_val"]
        < 0.95
    ):
        input_tap((1270, 494))
        time.sleep(2.0)


def go_outlets(name: str):
    """
    说明:
        前往指定门店
    参数:
        :param name: 门店名称
    """
    go_city()
    logger.info(f"前往 => {name}")
    if result := blurry_ocr_click(name, excursion_pos=(-2, 50), log=False):
        return result
    input_swipe((969, 369), (457, 340), time=500)
    if result := blurry_ocr_click(name, excursion_pos=(-2, 50), log=False):
        return result
    input_swipe((641, 246), (637, 615), time=500)
    if result := blurry_ocr_click(name, excursion_pos=(-2, 50)):
        return result


def go_home():
    """
    说明:
        返回主界面
    """
    logger.info("返回主界面")
    while match_screenshot(screenshot(), "resources/main_map.png")["max_val"] < 0.96:
        time.sleep(1)
        input_tap((228, 27))


def wait_fight_end():
    """
    说明:
        等待战斗结束
    """
    logger.info("等待战斗结束")
    start = time.perf_counter()
    while time.perf_counter() - start < FIGHT_TIME:
        bgrs = get_bgrs(
            screenshot(), [(1114, 630), (1204, 624), (236, 26), (1134, 628)]
        )
        logger.debug(f"等待战斗结束颜色检查: {bgrs}")
        if BGRGroup([198, 200, 200], [202, 204, 204]) == bgrs[0] and BGRGroup(
            [183, 185, 185], [187, 189, 189] == bgrs[1]
        ):
            logger.info("检测到执照等级提升")
            input_tap((1151, 626))
            continue
        elif (
            BGRGroup([245, 245, 245], [255, 255, 255]) == bgrs[0]
            and BGRGroup([0, 0, 0], [10, 10, 10]) == bgrs[1]
        ):
            logger.info("战斗胜利")
            time.sleep(1.0)
            input_tap((1151, 626))
            return True
        elif (
            BGRGroup([245, 245, 245], [255, 255, 255]) == bgrs[0]
            and BGRGroup([9, 9, 9], [10, 10, 10]) == bgrs[3]
        ):
            logger.info("战斗失败")
            time.sleep(1.0)
            input_tap((1151, 626))
            return True
        elif bgrs[2] == [124, 126, 125]:
            logger.info("开启自动战斗")
            input_tap((233, 44))
        time.sleep(3)
    logger.error("战斗超时")
    return False
