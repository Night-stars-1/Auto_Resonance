"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-05 17:24:47
LastEditTime: 2025-02-11 22:14:21
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time

from loguru import logger

from core.control.control import input_tap, screenshot
from core.model.config import config
from core.module.bgr import BGR
from core.preset.control import go_home
from core.utils.utils import RESOURCES_PATH

FIGHT_TIME = 300
MAP_WAIT_TIME = 3000

# pick_mask = cv.imread("resources/mask/pick_mask.png", cv.IMREAD_GRAYSCALE)
# _, pick_mask = cv.threshold(pick_mask, 128, 255, cv.THRESH_BINARY)


class STATION:

    def __init__(self, station: bool, is_destine: bool = False) -> None:
        """
        站点类

        :param station: 是否操作成功
        :param is_destine: 是否在目标站点
        :param cur_station: 当前站点
        :param tar_station: 目标站点
        """
        self.station = station
        self.is_destine = is_destine

    def __bool__(self) -> bool:
        return self.station

    def wait(self):
        """
        说明:
            等待进入站点
        """
        if self.station == False:
            logger.error("进入列车行驶状态失败")
            return False
        if self.is_destine:
            return True
        logger.info("进入行车监听")
        start = time.perf_counter()
        while time.perf_counter() - start < MAP_WAIT_TIME:
            image = screenshot()
            # 0-2攻击检测，3-4拦截检测
            attack_bgrs = image.get_bgrs(
                [(944, 247), (967, 229), (1056, 229), (1103, 328), (1128, 332)]
            )
            reach_bgrs = image.get_bgrs(
                [(839, 354), (814, 359), (1051, 641), (658, 690)]
            )
            run_bgr = image.get_bgr((1225, 481))
            logger.debug(f"行车攻击检测: {attack_bgrs}")
            logger.debug(f"行车检测: {reach_bgrs}")
            logger.debug(f"是否进站检测: {run_bgr}")
            if (
                BGR(8, 168, 234) <= attack_bgrs[0] <= BGR(10, 171, 245)
                and BGR(8, 168, 234) <= attack_bgrs[1] <= BGR(10, 171, 245)
                and BGR(8, 168, 234) <= attack_bgrs[2] <= BGR(10, 171, 245)
            ):
                logger.info("检测到拦截，进行攻击")
                self.join_wait_fight()
            elif (
                BGR(8, 168, 234) <= attack_bgrs[3] <= BGR(9, 171, 245)
                and BGR(8, 168, 234) <= attack_bgrs[4] <= BGR(9, 171, 245)
            ):
                logger.info("检测到可撞击")
            elif (
                BGR(20, 20, 20) <= reach_bgrs[0] <= BGR(25, 25, 25)
                and BGR(250, 250, 250) <= reach_bgrs[1] <= BGR(255, 255, 255)
            ):
                logger.info("站点到达")
                input_tap((877, 359))
                # go_home()
                return True
            elif BGR(251, 253, 253) == run_bgr:
                logger.info("站点到达")
                return True
            elif (
                reach_bgrs[2] == [251, 253, 253]
                and reach_bgrs[2] < BGR(235, 235, 250) 
                and reach_bgrs[2] > BGR(240, 240, 255)
                and config.global_config.is_speed
            ):
                logger.info("点击加速弹丸")
                input_tap((1061, 657))
                time.sleep(0.5)
            if config.global_config.is_auto_pick:
                input_tap((781, 484))  # 捡垃圾
            time.sleep(0.3)
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
            image = screenshot()
            image.crop_image((1032, 621), (1123, 708))
            retult = image.match_template(RESOURCES_PATH / "stations/speed_up.png", 0.95)
            if retult:
                return True
        return False

    def join_wait_fight(self):
        """
        说明:
            进入并等待攻击结束
        """
        time.sleep(0.5)
        input_tap((1009, 251))
        time.sleep(1)
        for _ in range(3):
            image = screenshot()
            image.crop_image((1133, 132), (1268, 610))
            result = image.match_template(RESOURCES_PATH / "fight/start_fight.png", 0.95)
            if result:
                input_tap(result.loc)
                logger.info("加入攻击成功, 进入战斗监听")
                break
            else:
                logger.error("加入战斗失败")
            time.sleep(1)
        # 等待战斗结束
        start = time.perf_counter()
        while time.perf_counter() - start < FIGHT_TIME:
            image = screenshot()
            bgrs = image.get_bgrs([(1114, 630), (1204, 624), (159, 26)])
            logger.debug(f"战斗检测: {bgrs}")
            if (
                BGR(198, 200, 200) <= bgrs[0] <= BGR(202, 204, 204)
                and BGR(183, 185, 185) <= bgrs[1] <= BGR(187, 189, 189)
            ):
                logger.info("检测到执照等级提升")
                input_tap((1151, 626))
            elif image.crop_image((1137, 566), (1224, 652)).match_template(
                RESOURCES_PATH / "fight/end_fight.png", 0.995
            ):
                logger.info("战斗结束")
                time.sleep(1.5)
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
            elif bgrs[2] == [126, 126, 126]:
                logger.info("开启自动战斗")
                input_tap((159, 44))
            time.sleep(3)
        logger.error("战斗超时")
        return False
