import time

from core.adb import input_tap, screenshot
from core.image import get_bgr
from core.presets.presets import go_home, go_outlets


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


def attack_boss():
    click_task()
