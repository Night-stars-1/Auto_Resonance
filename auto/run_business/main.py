import time
from loguru import logger
from typing import Literal

from core.adb import input_tap, screenshot
from core.image import get_bgr
from core.presets import go_outlets, wait


def go_business(type: Literal["buy", "sell"] = "buy"):
    result = go_outlets("交易所")
    is_join = wait("resources/shop/business_notes.png", cropped_pos1=(242, 11), cropped_pos2=(414, 66))
    if result and is_join:
        if type == "buy":
            input_tap((927, 321))
        elif type == "sell":
            input_tap((932, 404))
        time.sleep(1.0)
        bgr = get_bgr(screenshot(), (1175, 460))
        logger.debug(f"进入交易所颜色检查: {bgr}")
        if bgr == [2, 133, 253] or bgr == [0, 183, 253] or bgr == [251, 253, 253]:
            return True
        else:
            logger.error("进入交易所失败")
            return False
    else:
        logger.error("进入交易所失败")
        return False
