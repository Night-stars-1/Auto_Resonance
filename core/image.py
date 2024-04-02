import cv2 as cv

from loguru import logger
from typing import Tuple, Optional

def crop_image(screenshot, crop_coords):
    """
    说明:
        截取图片
    参数:
        :param screenshot: 截图
        :param crop_coords: 截取坐标 (y_start, y_end, x_start, x_end)
    """
    return screenshot[crop_coords[0] : crop_coords[1], crop_coords[2] : crop_coords[3]]


def match_screenshot(screenshot: cv.typing.MatLike, template_path: str, cropped_pos: Tuple[int, int, int, int]=(0, 0, 0, 0)) -> dict:
    """
    说明：
        比对图片
    参数：
        :param screenshot: 屏幕截图
        :param template_path: 目标图片
        :param cropped_pos: 切剪区域 (x1, x2, y1, y2)
    """
    if cropped_pos != (0, 0, 0, 0):
        screenshot = screenshot[cropped_pos[2]:cropped_pos[3], cropped_pos[0]:cropped_pos[1]]
    template = cv.imread(template_path)
    result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)
    length, width, __ = template.shape
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    min_loc = (min_loc[0]+cropped_pos[0], min_loc[1]+cropped_pos[2])
    max_loc = (max_loc[0]+cropped_pos[0], max_loc[1]+cropped_pos[2])
    logger.debug(f"{min_val=}, {max_val=}, {min_loc=}, {max_loc=}")
    return {
        "min_val": min_val,
        "max_val": max_val,
        "min_loc": (
            min_loc[0] + (width / 2),
            min_loc[1] + (length / 2),
        ),
        "max_loc": (
            max_loc[0] + (width / 2),
            max_loc[1] + (length / 2),
        ),
    }


def show_image(screenshot, name="image"):
    cv.namedWindow(name)
    cv.imshow(name, screenshot)
    cv.waitKey(0)
    cv.destroyAllWindows()
