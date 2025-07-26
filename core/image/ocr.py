"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 21:40:57
LastEditTime: 2025-02-04 23:40:25
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Tuple, Union

import cv2 as cv
from loguru import logger
from onnxocr.onnx_paddleocr import ONNXPaddleOcr

from core.image.utils import crop_image

model = ONNXPaddleOcr(
    use_angle_cls=False, use_gpu=True, use_dml=False, use_openvino=False
)

def ocrout2result(out, cropped_pos1):
    out = out[0]
    # logger.debug(f"识别结果: {out}")
    return [
        {
            "text": predict_data[1][0],
            "score": predict_data[1][1],
            "position": [
                [
                    predict_data[0][0][0] + cropped_pos1[0],
                    predict_data[0][0][1] + cropped_pos1[1],
                ],
                [
                    predict_data[0][1][0] + cropped_pos1[0],
                    predict_data[0][1][1] + cropped_pos1[1],
                ],
                [
                    predict_data[0][2][0] + cropped_pos1[0],
                    predict_data[0][2][1] + cropped_pos1[1],
                ],
                [
                    predict_data[0][3][0] + cropped_pos1[0],
                    predict_data[0][3][1] + cropped_pos1[1],
                ],
            ],
        }
        for predict_data in out
    ]


def predict(
    image: Union[str, Path, cv.typing.MatLike],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    no_crop: bool = False
):
    """
    说明：
        OCR识别图片上的文字
    参数：
        :param img_fp: 图片
        :param cropped_pos1: 切剪区域 (x1, y1)
        :param cropped_pos2: 切剪区域 (x2, y2)
    """
    if isinstance(image, Path):
        image = str(image)
    if isinstance(image, str):
        image = cv.imread(image)
    if (cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0)) and not no_crop:
        image = crop_image(image, cropped_pos1, cropped_pos2)
    out = model.ocr(image)
    result = ocrout2result(out, cropped_pos1)
    logger.debug(result)
    return result


def number_predict(
    image: Union[str, Path, cv.typing.MatLike],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
    no_crop: bool = False
):
    """
    说明：
        OCR识别图片上的文字
    参数：
        :param img_fp: 图片
        :param cropped_pos: 切剪区域 (x1, x2, y1, y2)
    """
    if isinstance(image, Path):
        image = str(image)
    if isinstance(image, str):
        image = cv.imread(image)
    if (cropped_pos1 != (0, 0) or cropped_pos2 != (0, 0)) and not no_crop:
        image = crop_image(image, cropped_pos1, cropped_pos2)
    out = model.ocr(image)
    result = ocrout2result(out, cropped_pos1)
    logger.debug(result)
    return result
