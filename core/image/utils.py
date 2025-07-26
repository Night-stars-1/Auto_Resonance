from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Tuple, Union

import cv2 as cv
import numpy as np
from loguru import logger

from core.module.bgr import BGR
from core.module.hsv import HSV


@dataclass
class MATCH_TEMPLATE_RESULT:
    """
    模板匹配结果
    """

    score: float
    loc: Tuple[int, int]
    status: bool = True

    def __str__(self):
        return f"score: {self.score}, loc: {self.loc} status: {self.status}"

    def __bool__(self):
        return self.status

    def __eq__(self, value: object) -> bool:
        return self.status == bool(value)


def crop_image(
    image: cv.typing.MatLike,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
):
    """
    截取图片

    :param screenshot: 截图
    :param cropped_pos1: 切剪区域 (x1, y1)
    :param cropped_pos2: 切剪区域 (x2, y2)
    """
    if cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0):
        image = image[cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]]
    return image


def match_template(
    image: cv.typing.MatLike,
    template: Union[str, Path, cv.typing.MatLike],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    threshold: float = 0.8,
    no_crop: bool = False
) -> MATCH_TEMPLATE_RESULT:
    """
    比对图片

    :param screenshot: 屏幕截图
    :param template: 目标图片
    :param threshold: 最低相似度
    """
    if isinstance(template, Path):
        template = str(template)
    if isinstance(template, str):
        template = cv.imread(template)
    if (cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0)) and not no_crop:
        image = crop_image(image, cropped_pos1, cropped_pos2)
    result = cv.matchTemplate(image, template, cv.TM_CCORR_NORMED)
    length, width, __ = template.shape
    _, score, _, max_loc = cv.minMaxLoc(result)
    max_loc = (max_loc[0] + cropped_pos1[0], max_loc[1] + cropped_pos1[1])
    logger.debug(f"{score=} {max_loc=} status={score >= threshold}")
    return MATCH_TEMPLATE_RESULT(
        score=score,
        loc=(
            int(max_loc[0] + (width / 2)),
            int(max_loc[1] + (length / 2)),
        ),
        status=score >= threshold,
    )


def get_bgr(
    image: cv.typing.MatLike,
    pos=(0, 0),
    offset=0,
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    no_crop: bool = False
):
    """
    获取指定位置的BGR

    :param image: 图片
    :param pos: 位置 (x, y)
    """
    if (cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0)) and not no_crop:
        image = crop_image(image, cropped_pos1, cropped_pos2)
    pos = (pos[0] - cropped_pos1[0], pos[1] - cropped_pos1[1])
    color = image[pos[1], pos[0]]
    return BGR(*color, offset=offset)


def get_hsv(
    image: cv.typing.MatLike,
    pos=(0, 0),
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    no_crop: bool = False
):
    """
    获取指定位置的HSV

    :param image: 图片
    :param pos: 位置 (x, y)
    """
    if (cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0)) and not no_crop:
        image = crop_image(image, cropped_pos1, cropped_pos2)
    image_hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)

    pos = (pos[0] - cropped_pos1[0], pos[1] - cropped_pos1[1])
    color = image_hsv[int(pos[1]), int(pos[0])]
    return HSV(*color, offset=0)


def get_bgrs(
    image: cv.typing.MatLike,
    positions: List[Tuple[int, int]] = [(0, 0)],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    no_crop: bool = False
):
    """
    获取指定位置的颜色

    :param image: 图片
    :param pos: 位置 (x, y)
    """
    if (cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0)) and not no_crop:
        image = crop_image(image, cropped_pos1, cropped_pos2)
    new_positions = [
        (position[0] - cropped_pos1[0], position[1] - cropped_pos1[1])
        for position in positions
    ]
    new_positions: Any = [(position[1], position[0]) for position in positions]
    new_positions = np.array(new_positions)
    colors = image[new_positions[:, 0], new_positions[:, 1]]
    return [BGR(*color, offset=0) for color in colors]


def show_image(image: cv.typing.MatLike, name="image", time=0):
    """
    显示图片

    :param screenshot: 截图
    :param name: 窗口名称
    :param time: 显示时间
    """
    cv.namedWindow(name)
    cv.imshow(name, image)
    cv.waitKey(time)
    cv.destroyAllWindows()


def save_image(image: cv.typing.MatLike, path: Union[str, Path]):
    """
    保存图片

    :param screenshot: 截图
    :param path: 保存路径
    """
    if isinstance(path, Path):
        path = str(path)
    cv.imwrite(path, image)
    logger.info(f"图片已保存到 {path}")
