"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:18:15
LastEditTime: 2024-04-06 01:50:03
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import List, Tuple

import cv2 as cv
import numpy as np
from loguru import logger


def crop_image(
    screenshot,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
):
    """
    说明:
        截取图片
    参数:
        :param screenshot: 截图
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
    """
    return screenshot[
        cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
    ]


def match_screenshot(
    screenshot: cv.typing.MatLike,
    template_path: str,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
) -> dict:
    """
    说明：
        比对图片
    参数：
        :param screenshot: 屏幕截图
        :param template_path: 目标图片
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
    """
    if cropped_pos1 != (0, 0) and cropped_pos2 != (0, 0):
        screenshot = screenshot[
            cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
        ]
    template = cv.imread(template_path)
    result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)
    length, width, __ = template.shape
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    min_loc = (min_loc[0] + cropped_pos1[0], min_loc[1] + cropped_pos1[1])
    max_loc = (max_loc[0] + cropped_pos1[0], max_loc[1] + cropped_pos1[1])
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


def get_bgr(
    image,
    pos=(0, 0),
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
) -> List[int]:
    """
    说明:
        获取指定位置的颜色
    参数:
        :param image: 图片
        :param pos: 位置 (x, y)
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
    """
    if cropped_pos1 != (0, 0) and cropped_pos2 != (0, 0):
        image = image[
            cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
        ]
        pos = (pos[0] - cropped_pos1[0], pos[1] - cropped_pos1[1])
    color = image[pos[1], pos[0]]
    return color.tolist()


def get_bgrs(
    image,
    positions: List[Tuple[int, int]] = [(0, 0)],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
) -> List[List[int]]:
    """
    说明:
        获取指定位置的颜色
    参数:
        :param image: 图片
        :param pos: 位置 (x, y)
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
    """
    if cropped_pos1 != (0, 0) and cropped_pos2 != (0, 0):
        image = image[
            cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
        ]
        positions = [
            (position[0] - cropped_pos1[0], position[1] - cropped_pos1[1])
            for position in positions
        ]
    positions = [[position[1], position[0]] for position in positions]
    positions = np.array(positions)
    colors = image[positions[:, 0], positions[:, 1]]
    return colors.tolist()


def get_all_color_pos(
    image, threshold_lower=200, threshold_upper=255, min_area=80, max_area=150
):
    """
    说明:
        获取所有颜色区域的中心点
    参数:
        :param image: 图片
        :param threshold_lower: 阈值下限
        :param threshold_upper: 阈值上限
        :param min_area: 最小面积
        :param max_area: 最大面积
    """
    all_pos = []
    image = crop_image(image, cropped_pos1=(0, 66), cropped_pos2=(1280, 720))
    # 转换到灰度图
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 阈值处理找到指定颜色区域
    _, thresh = cv.threshold(gray, threshold_lower, threshold_upper, cv.THRESH_BINARY)

    # 寻找轮廓
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv.contourArea(contour)

        # 只处理指定面积的轮廓
        if min_area < area < max_area:
            # 计算每个轮廓的边界框
            x, y, w, h = cv.boundingRect(contour)
            all_pos.append((x + (w / 2), y + (h / 2) + 66))

    return all_pos


def show_image(screenshot, name="image", time=0):
    """
    说明:
        显示图片
    参数:
        :param screenshot: 截图
        :param name: 窗口名称
        :param time: 显示时间
    """
    cv.namedWindow(name)
    cv.imshow(name, screenshot)
    cv.waitKey(time)
    cv.destroyAllWindows()
