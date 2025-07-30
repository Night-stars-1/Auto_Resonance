"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:18:15
LastEditTime: 2025-02-04 23:18:27
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import List, Tuple, Union

import cv2 as cv
from loguru import logger

from core.image.ocr import number_predict, predict
from core.image.utils import MATCH_TEMPLATE_RESULT, crop_image, get_bgr, get_bgrs, get_hsv, match_template, save_image, show_image
from core.module.bgr import BGR


class Image:
    def __init__(self, image: cv.typing.MatLike):
        self.image = image
        self.cropped_pos1 = (0, 0)
        self.cropped_pos2 = (0, 0)

    def crop_image(
        self,
        cropped_pos1: Tuple[int, int] = (0, 0),
        cropped_pos2: Tuple[int, int] = (0, 0),
    ):
        """
        截取图片

        :param screenshot: 截图
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
        """
        self.cropped_pos1 = cropped_pos1
        self.cropped_pos2 = cropped_pos2
        self.image = crop_image(self.image, cropped_pos1, cropped_pos2)
        return self

    def match_template(
        self,
        template: Union[str, Path, cv.typing.MatLike],
        threshold: float = 0.8,
    ) -> MATCH_TEMPLATE_RESULT:
        """
        比对图片

        :param screenshot: 屏幕截图
        :param template: 目标图片
        :param threshold: 最低相似度
        """
        return match_template(self.image, template, self.cropped_pos1, self.cropped_pos2, threshold, no_crop=True)

    def get_bgr(
        self,
        pos=(0, 0),
        offset=0,
    ):
        """
        获取指定位置的BGR

        :param image: 图片
        :param pos: 位置 (x, y)
        """
        return get_bgr(self.image, pos, offset, self.cropped_pos1, self.cropped_pos2, no_crop=True)

    def get_hsv(
        self,
        pos=(0, 0),
    ):
        """
        获取指定位置的HSV

        :param image: 图片
        :param pos: 位置 (x, y)
        """
        return get_hsv(self.image, pos, self.cropped_pos1, self.cropped_pos2, no_crop=True)

    def get_bgrs(self, positions: List[Tuple[int, int]] = [(0, 0)]):
        """
        获取指定位置的颜色

        :param image: 图片
        :param pos: 位置 (x, y)
        """
        return get_bgrs(self.image, positions, self.cropped_pos1, self.cropped_pos2, no_crop=True)

    def show_image(self, name="image", time=0):
        """
        显示图片

        :param screenshot: 截图
        :param name: 窗口名称
        :param time: 显示时间
        """
        show_image(self.image, name, time)

    def save_image(self, path: Union[str, Path]):
        """
        保存图片

        :param screenshot: 截图
        :param path: 保存路径
        """
        save_image(self.image, path)

    def ocr(self):
        return predict(self.image, self.cropped_pos1, self.cropped_pos2, no_crop=True)

    def number_ocr(self):
        return number_predict(self.image, self.cropped_pos1, self.cropped_pos2, no_crop=True)