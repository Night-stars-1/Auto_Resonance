"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:24:47
LastEditTime: 2024-04-23 00:08:35
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.adb import input_tap, screenshot
from core.image import get_bgr, get_bgrs, match_screenshot
from core.models.config import config
from core.utils import compare_ranges

FIGHT_TIME = 300
MAP_WAIT_TIME = 3000


class STATION:
    """
    说明:
        站点类
    """

    def __init__(self, station: bool, is_destine: bool = False) -> None:
        self.station = station
        self.is_destine = is_destine

    def __bool__(self) -> bool:
        return self.station

    def wait(self):
        """
        说明:
            等待进入站点
        """
        if self.is_destine:
            return True
        logger.info("进入行车监听")
        start = time.perf_counter()
        while time.perf_counter() - start < MAP_WAIT_TIME:
            image = screenshot()
            attack_bgrs = get_bgrs(image, [(944, 247), (967, 229), (1056, 229)])
            reach_bgrs = get_bgrs(
                image, [(839, 354), (814, 359), (1051, 641), (658, 690)]
            )
            logger.debug(f"行车检测: {reach_bgrs}")
            if (
                compare_ranges([8, 168, 234], attack_bgrs[0], [9, 171, 245])
                and compare_ranges([8, 168, 234], attack_bgrs[1], [9, 171, 245])
                and compare_ranges([8, 168, 234], attack_bgrs[2], [9, 171, 245])
            ):
                logger.info("检测到拦截，进行攻击")
                self.join_wait_fight()
            elif compare_ranges(
                [20, 20, 20], reach_bgrs[0], [25, 25, 25]
            ) and compare_ranges([250, 250, 250], reach_bgrs[1], [255, 255, 255]):
                logger.info("站点到达")
                input_tap((877, 359))
                self.wait_home()
                return True
            elif (
                reach_bgrs[2] == [251, 253, 253]
                and not compare_ranges([235, 235, 250], reach_bgrs[2], [240, 240, 255])
                and config.global_config.isSpeed
            ):
                logger.info("点击加速弹丸")
                input_tap((1061, 657))
            time.sleep(1)
        logger.error("站点超时")
        return False

    def wait_join(self):
        """
        说明:
            等待进入行车地图
        """
        logger.info("等待进入行车地图")
        start = time.perf_counter()
        while time.perf_counter() - start < 10:
            retult = match_screenshot(
                screenshot(),
                "resources/stations/speed_up.png",
                cropped_pos1=(1032, 621),
                cropped_pos2=(1123, 708),
            )
            if retult["max_val"] > 0.95:
                return True
        return False

    def join_wait_fight(self):
        """
        说明:
            进入并等待攻击结束
        """
        input_tap((1009, 251))
        time.sleep(1)
        for _ in range(3):
            result = match_screenshot(
                screenshot(),
                "resources/fight/start_fight.png",
                cropped_pos1=(1133, 132),
                cropped_pos2=(1268, 610),
            )
            if result["max_val"] > 0.95:
                input_tap(result["max_loc"])
                logger.info("加入攻击成功, 进入战斗监听")
                break
            else:
                logger.info("加入战斗失败")
            time.sleep(1)
        # 等待战斗结束
        start = time.perf_counter()
        while time.perf_counter() - start < FIGHT_TIME:
            bgrs = get_bgrs(screenshot(), [(1114, 630), (1204, 624), (236, 26)])
            if compare_ranges(
                [198, 200, 200], bgrs[0], [202, 204, 204]
            ) and compare_ranges([183, 185, 185], bgrs[1], [187, 189, 189]):
                logger.info("检测到执照等级提升")
                input_tap((1151, 626))
            if compare_ranges(
                [245, 245, 245], bgrs[0], [255, 255, 255]
            ) and compare_ranges([0, 0, 0], bgrs[1], [10, 10, 10]):
                logger.info("战斗结束")
                time.sleep(0.5)
                input_tap((1151, 626))
                return True
            elif bgrs[2] == [124, 126, 125]:
                logger.info("开启自动战斗")
                input_tap((233, 44))
            time.sleep(3)
        logger.error("战斗超时")
        return False

    def wait_home(self):
        """
        说明:
            等待返回主界面
        """
        while (
            match_screenshot(screenshot(), "resources/main_map.png")["max_val"] < 0.95
        ):
            time.sleep(3)
            input_tap((228, 27))
