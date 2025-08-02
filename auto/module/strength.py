from loguru import logger
from core.control.control import screenshot
from core.module.bgr import BGR
from core.preset.control import click, ocr_click, wait_gbr


def check_shop_strength():
    image = screenshot()
    image.crop_image((959, 13), (1036, 38))
    text = image.ocr()
    if len(text) == 0:
        return True
    strength = text[0]["text"].split("/")
    cur_strength = int(strength[0])
    total__strength = int(strength[1])
    return total__strength - cur_strength > 60

def use_food():
    click((1107, 606))
    if not wait_gbr(
        (61, 130),
        BGR(26, 38, 91),
        BGR(26, 38, 91)
    ):
        logger.error("未找到便当页面")
        return False
    click((1077, 430))
    status = ocr_click("确认", cropped_pos1=(952, 485), cropped_pos2=(1022, 522))
    click((1077, 430))
    return status


def use_candy():
    click((655, 242))
    return ocr_click("补充", cropped_pos1=(952, 565), cropped_pos2=(1023, 602))

def use_strength():
    if not wait_gbr(
        (522, 110),
        BGR(30, 40, 105),
        BGR(40, 50, 115),
        cropped_pos1=(482, 92),
        cropped_pos2=(562, 134),
    ):
        logger.error("未找到体力页面")
        return False
    # image = screenshot()
    # has_food = image.get_bgr((1052, 426))
    # if has_food:
    #     return use_food()
    return use_candy()
