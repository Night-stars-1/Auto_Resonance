"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-25 23:03:02
LastEditTime: 2024-05-11 21:44:17
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.adb import connect, input_swipe, input_tap, screenshot
from core.image import get_bgr, get_bgrs
from core.module.bgr import BGR
from core.ocr import predict
from core.presets import go_home


def get_skill_level_list():
    """
    说明:
        获取所有角色的共振开启数量列表
    """
    levels = []
    bgrs = get_bgrs(
        screenshot(), [(946, 173), (941, 276), (1052, 276), (1048, 176), (994, 239)]
    )
    logger.debug(f"角色共振等级颜色检测: {bgrs}")
    for bgr in bgrs:
        if bgr.r > 200:
            levels.append(True)
    return levels


def get_skill_level():
    """
    说明:
        获取所有角色的共振等级
    返回:
        :return: skill_level: dict: {角色名: 共振等级}
    """
    skill_level = {}
    start_time = time.perf_counter()
    while run_time := time.perf_counter() - start_time:
        if run_time > 1200:
            logger.error(f"扫描时间过长，强制停止")
            break
        input_tap((1255, 87))
        time.sleep(1)
        input_tap((992, 205))
        time.sleep(0.5)
        result = predict(screenshot(), cropped_pos1=(228, 134), cropped_pos2=(371, 168))
        if len(result) > 0:
            role_name = result[0]["text"]
            input_tap((1252, 456))
            time.sleep(0.5)
            input_tap((1252, 456))
            time.sleep(0.5)
            levels = get_skill_level_list()
            if role_name not in skill_level:
                skill_level[role_name] = len(levels)
            else:
                logger.info(f"发现重复角色可能已经识别完成，停止识别")
                return skill_level
            logger.info(f"{role_name}: {len(levels)}")
        input_swipe((658, 359), (116, 374), time=500)
        time.sleep(0.5)
    return skill_level


def run():
    status = connect()
    if not status:
        logger.error("ADB连接失败")
        return {}
    go_home()
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < 10:
        input_tap((1274, 47))
        bgr = get_bgr(
            screenshot(), (162, 365), cropped_pos1=(147, 349), cropped_pos2=(191, 382)
        )
        logger.debug(f"是否进入角色界面颜色检查: {bgr}")
        if BGR(155, 155, 155) == bgr:
            input_tap((91, 174))  # 点击角色
            break
    time.sleep(1)
    logger.info("开始扫描")
    skill_level = get_skill_level()
    logger.info("扫描完成")
    return skill_level
