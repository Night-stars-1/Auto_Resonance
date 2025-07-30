"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:24:47
LastEditTime: 2025-02-11 19:26:36
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Dict, Optional, Tuple

from loguru import logger

from core.control.control import (
    input_swipe,
    input_tap,
    screenshot,
    screenshot_image,
    wait_stopped,
)
from core.module.bgr import BGR
from core.image.ocr import predict
from core.preset import blurry_ocr_click, go_home
from core.utils.utils import RESOURCES_PATH, read_json

from .control import click_image, ocr_click
from .station import STATION

FIGHT_TIME = 1000

STATION_NAME2PNG: Dict[str, str] = read_json(RESOURCES_PATH / "stations/name2id.json")

# 站点坐标，左上角为(0, 0)
# STATION_POS_DATA = {
#     "澄明数据中心": (1049, 345),
#     "7号自由港": (665, 577),
#     "阿妮塔战备工厂": (832, 664),
#     "阿妮塔发射中心": (164, 420 + 577),
#     "阿妮塔能源研究所": (614, 454 + 577),
#     "修格里城": (285 + 1049, 121 + 345),
#     "铁盟哨站": (501 + 1049, 122 + 345),
#     "荒原站": (753 + 1049, 121 + 345),
#     "曼德矿场": (602 + 1049, 322 + 345),
#     "淘金乐园": (701 + 1049, 604 + 345),
#     "海角城": (164 + 293, 420 + 577 + 569),
# }
STATION_POS_DATA: Dict[str, Tuple[int, int]] = read_json(
    RESOURCES_PATH / "goods/CityPosData.json"
)


def calculate_station_differences(station_map_data: dict):
    differences = {}
    for site1, coords1 in station_map_data.items():
        for site2, coords2 in station_map_data.items():
            if site1 != site2:
                x_diff = coords2[0] - coords1[0]
                y_diff = coords1[1] - coords2[1]
                differences[(site1, site2)] = (x_diff, y_diff)
    return differences


# 计算站点之间的差值
STATION_DIFFERENCES = calculate_station_differences(STATION_POS_DATA)


def click_station(name: str, cur_station: Optional[str] = None):
    """
    点击站点, 该滑动通过站点间相对距离完成

    :param name: 目标站点
    :param cur_station: 当前站点
    """
    logger.info(f"点击站点 => {name}")
    if screenshot().match_template(RESOURCES_PATH / "main_map.png", 0.95) == False:
        logger.info("未检测到主地图界面，返回主地图")
        go_home()
    logger.info("检测到主地图界面，识别站点")
    if not cur_station:
        station = get_station(is_go_home=False)
    else:
        station = cur_station
    if name == station:
        logger.info("已在目标站点")
        return STATION(True, is_destine=True)
    else:
        go_home()

    if name not in STATION_NAME2PNG:
        raise ValueError(f"未找到站点 {name} 的图片")
    city_differences = STATION_DIFFERENCES.get((station, name))
    if city_differences:
        # 点击地图
        input_tap((1201, 666))
        # 等待地图打开
        time.sleep(0.5)
        wait_stopped(threshold=7100000)

        source_x = 640
        source_y = 360
        # 如果有路线则进行寻找
        x1 = source_x + city_differences[0] / 2.5
        y1 = source_y + city_differences[1] / 2.5

        # 滑动到目标站点
        input_swipe((x1, y1), (source_x, source_y), swipe_time=800)
        # 向回拖动避免画面长时间移动
        input_swipe(
            (source_x, source_y), (source_x - 10, source_y - 10), swipe_time=500
        )
        wait_stopped(threshold=7100000)  # 等待滑动完成

        image = screenshot()
        image.crop_image((0, 0), (1280, 654))
        result = image.match_template(
            RESOURCES_PATH / "stations" / STATION_NAME2PNG[name], 0.95
        )
        if result:
            # 点击站点
            input_tap(result.loc)
        else:
            logger.info(f"未找到站点 {name}，尝试OCR识别")
            if not ocr_click(name):
                logger.error(f"未找到站点: {name}")
                return STATION(False)
        time.sleep(0.5)
        # 点击前往目的地按钮
        logger.info("点击前往目的地按钮")
        if click_image(
            RESOURCES_PATH / "map/go_station.png",
            cropped_pos1=(937, 605),
            cropped_pos2=(1218, 679),
            trynum=5,
        ):
            time.sleep(1.0)
            click_image(
                RESOURCES_PATH / "map/join_station.png",
                cropped_pos1=(719, 405),
                cropped_pos2=(927, 485),
                trynum=5,
            )
            return STATION(True)
        else:
            logger.error(f"未找到前往目的地按钮: {name}")
    else:
        logger.error("没有该站点的坐标信息")
    return STATION(False)


def get_station(is_go_home: bool = True):
    """
    获取当前站点

    :param is_go_home: 是否返回主界面
    """
    go_home()
    input_tap((1170, 493))
    time.sleep(1.0)
    reslut = predict(
        screenshot_image(), cropped_pos1=(166, 520), cropped_pos2=(470, 600)
    )
    if len(reslut) == 0:
        raise ValueError("未识别到当前城市")
    logger.info(f"当前站点: {reslut[0]['text']}")
    if is_go_home:
        # 返回主界面，回溯进入城市地图操作
        go_home()
    return reslut[0]["text"]


def go_city():
    """
    说明:
        进入城市界面
    """
    while (
        screenshot()
        .crop_image(cropped_pos1=(25, 634), cropped_pos2=(99, 707))
        .match_template(RESOURCES_PATH / "fame.png", 0.95)
        == False
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
    if result := blurry_ocr_click(name, excursion_pos=(0, 80), log=False):
        return result
    input_swipe((457, 340), (457, 369), swipe_time=500)
    if result := ocr_click(name, excursion_pos=(0, 80), log=False):
        return result
    input_swipe((400, 340), (457, 340), swipe_time=500)
    if result := ocr_click(name, excursion_pos=(0, 80), log=False):
        return result
    input_swipe((969, 369), (457, 340), swipe_time=500)
    if result := ocr_click(name, excursion_pos=(0, 80), log=False):
        return result
    input_swipe((641, 246), (637, 615), swipe_time=500)
    if result := ocr_click(name, excursion_pos=(0, 80)):
        return result


def wait_fight_end():
    """
    说明:
        等待战斗结束
    """
    logger.info("等待战斗结束")
    start = time.perf_counter()
    while time.perf_counter() - start < FIGHT_TIME:
        image = screenshot()
        bgrs = image.get_bgrs([(1114, 630), (1204, 624), (167, 29)])
        logger.debug(f"等待战斗结束颜色检查: {bgrs}")
        if (
            BGR(198, 200, 200) <= bgrs[0] <= BGR(202, 204, 204) 
            and BGR(183, 185, 185) <= bgrs[1] <= BGR(187, 189, 189)
        ):
            logger.info("检测到执照等级提升")
            input_tap((1151, 626))
            continue
        elif image.crop_image((1070, 600), (1251, 670)).match_template(
            RESOURCES_PATH / "fight/end_fight.png", 0.995
        ):
            logger.info("战斗结束")
            time.sleep(1.0)
            input_tap((1151, 626))
            return True
        # elif (
        #     BGRGroup([245, 245, 245], [255, 255, 255]) == bgrs[0]
        #     and BGRGroup([9, 9, 9], [10, 10, 10]) == bgrs[3]
        # ):
        #     logger.info("战斗失败")
        #     time.sleep(1.0)
        #     input_tap((1151, 626))
        #     return True
        elif bgrs[2] == [124, 126, 125]:
            logger.info("开启自动战斗")
            input_tap((233, 44))
        time.sleep(3)
    logger.error("战斗超时")
    return False
