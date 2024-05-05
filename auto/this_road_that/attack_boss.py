import time
from typing import Dict

from loguru import logger

from core.adb import connect, input_tap, screenshot
from core.image import get_bgr
from core.module.bgr import BGR, BGRGroup
from core.presets import (
    click,
    click_image,
    go_home,
    go_outlets,
    wait_fight_end as _wait_fight_end,
)


def click_task():
    """
    说明:
        点击清缴任务
    """
    go_home()
    go_outlets("工程援助中心")
    while BGR(251, 126, 65) != get_bgr(
        screenshot(), (300, 669), cropped_pos1=(289, 640), cropped_pos2=(424, 701)
    ):
        time.sleep(0.5)
    input_tap((837, 322))
    time.sleep(0.5)


def wait_fight_end():
    _wait_fight_end()
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < 10:
        bgr = get_bgr(
            screenshot(), (960, 98), cropped_pos1=(851, 75), cropped_pos2=(1022, 124)
        )
        if BGR(240, 125, 65) == bgr:
            break


def attack_one(num: int = 1):
    input_tap((154, 176))
    for n in range(num):
        logger.info(f"开始攻击寒潮浮囊体 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if BGRGroup((20, 180, 240), (55, 210, 255)) == bgr:
            input_tap((1006, 649))
            click_image(
                "railway_safety_bureau/start_attack.png",
                (1133, 128),
                (1263, 628),
                trynum=10,
            )
            wait_fight_end()
        else:
            logger.info("攻击次数用完，退出攻击")
            break


def attack_two(num: int = 1):
    input_tap((674, 181))
    for n in range(num):
        logger.info(f"开始攻击昏恶巨象 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if BGRGroup([20, 180, 240], [55, 210, 255]) == bgr:
            input_tap((1006, 649))
            click_image(
                "railway_safety_bureau/start_attack.png",
                (1133, 128),
                (1263, 628),
                trynum=10,
            )
            wait_fight_end()
        else:
            logger.info("攻击次数用完，退出攻击")
            break


def attack_three(num: int = 1):
    input_tap((155, 462))
    for n in range(num):
        logger.info(f"开始攻击尘鸣游磷 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if BGRGroup([20, 180, 240], [55, 210, 255]) == bgr:
            input_tap((1006, 649))
            click_image(
                "railway_safety_bureau/start_attack.png",
                (1133, 128),
                (1263, 628),
                trynum=10,
            )
            wait_fight_end()
        else:
            logger.info("攻击次数用完，退出攻击")
            break


def attack_four(num: int = 1):
    input_tap((679, 505))
    for n in range(num):
        logger.info(f"开始攻击劫掠者-执桔 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if BGRGroup([20, 180, 240], [55, 210, 255]) == bgr:
            input_tap((1006, 649))
            click_image(
                "railway_safety_bureau/start_attack.png",
                (1133, 128),
                (1263, 628),
                trynum=10,
            )
            wait_fight_end()
        else:
            logger.info("攻击次数用完，退出攻击")
            break


def attack_five(num: int = 1):
    input_tap((405, 317))
    for n in range(num):
        logger.info(f"开始攻击裂首骨龙 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if BGRGroup([20, 180, 240], [55, 210, 255]) == bgr:
            input_tap((1006, 649))
            click_image(
                "railway_safety_bureau/start_attack.png",
                (1133, 128),
                (1263, 628),
                trynum=10,
            )
            wait_fight_end()
        else:
            logger.info("攻击次数用完，退出攻击")
            break


def attack_boss(num: int = 1, bossList: Dict[str, str] = {}):
    status = connect()
    if not status:
        logger.error("ADB连接失败")
        return False
    click_task()
    click((883, 540))
    for boss_name, boss in bossList.items():
        try:
            globals().get(boss)(num)
        except AttributeError:
            logger.error(f"未找到对应的BOSS: {boss_name}")
