"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:18:15
LastEditTime: 2024-04-29 19:43:59
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import List, Tuple

import cv2 as cv
import numpy as np
from loguru import logger

from core.module.bgr import BGR
from core.module.hsv import HSV


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
):
    """
    说明:
        获取指定位置的BGR
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
    return BGR(*color, offset=0)


def get_hsv(
    image,
    pos=(0, 0),
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
):
    """
    说明:
        获取指定位置的HSV
    参数:
        :param image: 图片
        :param pos: 位置 (x, y)
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
    """
    image_hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)
    if cropped_pos1 != (0, 0) and cropped_pos2 != (0, 0):
        image_hsv = image_hsv[
            cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
        ]
        pos = (pos[0] - cropped_pos1[0], pos[1] - cropped_pos1[1])
    color = image_hsv[int(pos[1]), int(pos[0])]
    return HSV(*color, offset=0)


def get_bgrs(
    image,
    positions: List[Tuple[int, int]] = [(0, 0)],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
):
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
    return [BGR(*color, offset=0) for color in colors]


def get_all_color_pos(
    image, threshold_lower=200, threshold_upper=255, min_area=40, max_area=150
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


def find_icons_coordinates(image, icon_path, threshold=0.8, min_distance=10):
    """
    说明:
        在给定图像中找到所有与模板匹配的图标的坐标，并过滤掉过近的坐标。
    参数:
        :param image: 要搜索的图像
        :param icon_path: 要匹配的图标
        :param threshold: 匹配阈值，介于0和1之间
        :param min_distance: 最小允许的距离
        :return: 找到的图标的坐标列表
    """
    image = image.copy()
    img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    template = cv.imread(icon_path)
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    w, h = template_gray.shape[::-1]

    # 模板匹配
    res = cv.matchTemplate(img_gray, template_gray, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    coordinates = []
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        coordinates.append((pt[0], pt[1]))  # 只添加左上角坐标

    # 过滤过近的匹配
    filtered = []
    for coord in coordinates:
        too_close = False
        for fcoord in filtered:
            distance = (
                (fcoord[0] - coord[0]) ** 2 + (fcoord[1] - coord[1]) ** 2
            ) ** 0.5
            if distance < min_distance:
                too_close = True
                break
        if not too_close:
            filtered.append(coord)
    return filtered
