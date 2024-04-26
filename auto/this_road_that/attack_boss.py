import time

from loguru import logger

from core.adb import connect, input_tap, screenshot
from core.image import get_bgr
from core.presets import (
    click,
    click_image,
    click_station,
    find_text,
    go_home,
    go_outlets,
    wait,
    wait_fight_end as _wait_fight_end,
    wait_time,
)
from core.utils import compare_ranges


def click_task():
    """
    说明:
        点击清缴任务
    """
    go_home()
    go_outlets("工程援助中心")
    while get_bgr(
        screenshot(), (300, 669), cropped_pos1=(289, 640), cropped_pos2=(424, 701)
    ) != [251, 126, 65]:
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
        if compare_ranges([235, 120, 60], bgr, [245, 130, 70]):
            break

def attack_one(num: int = 1):
    input_tap((154, 176))
    for n in range(num):
        logger.info(f"开始攻击寒潮浮囊体 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if compare_ranges([20, 180, 240], bgr, [55, 210, 255]):
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
        if compare_ranges([20, 180, 240], bgr, [55, 210, 255]):
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
        if compare_ranges([20, 180, 240], bgr, [55, 210, 255]):
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
        if compare_ranges([20, 180, 240], bgr, [55, 210, 255]):
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
    input_tap((679, 505))
    for n in range(num):
        logger.info(f"开始攻击裂首骨龙 => {n+1}")
        time.sleep(0.5)
        bgr = get_bgr(
            screenshot(), (1000, 644), cropped_pos1=(852, 615), cropped_pos2=(1264, 678)
        )
        if compare_ranges([20, 180, 240], bgr, [55, 210, 255]):
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

def attack_boss(order: str, path: str, num: int = 1):
    status = connect(order, path)
    if not status:
        logger.error("ADB连接失败")
        return False
    click_task()
    click((883, 540))
    attack_one(num)
    attack_two(num)
    attack_three(num)
    attack_four(num)
    attack_five(num)
