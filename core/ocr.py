"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 21:40:57
LastEditTime: 2024-04-21 22:59:43
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Tuple, Union

import numpy as np
from cnocr import CnOcr
from PIL import Image

ocr = CnOcr(rec_root="resources/model/cnocr", det_root="resources/model/cnstd")
number_ocr = CnOcr(
    "number-densenet_lite_136-fc",
    rec_root="resources/model/cnocr",
    det_root="resources/model/cnstd",
)


def ocrout2result(out, cropped_pos1):
    return [
        {
            "text": predict_data["text"],
            "score": predict_data["score"],
            "position": [
                [
                    predict_data["position"][0][0] + cropped_pos1[0],
                    predict_data["position"][0][1] + cropped_pos1[1],
                ],
                [
                    predict_data["position"][1][0] + cropped_pos1[0],
                    predict_data["position"][1][1] + cropped_pos1[1],
                ],
                [
                    predict_data["position"][2][0] + cropped_pos1[0],
                    predict_data["position"][2][1] + cropped_pos1[1],
                ],
                [
                    predict_data["position"][3][0] + cropped_pos1[0],
                    predict_data["position"][3][1] + cropped_pos1[1],
                ],
            ],
        }
        for predict_data in out
    ]


def predict(
    img_fp: Union[str, Path, Image.Image, np.ndarray],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
):
    """
    说明：
        OCR识别图片上的文字
    参数：
        :param img_fp: 图片
        :param cropped_pos: 切剪区域 (x1, x2, y1, y2)
    """
    if cropped_pos1 != (0, 0) and cropped_pos2 != (0, 0):
        img_fp = img_fp[
            cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
        ]
    out = ocr.ocr(img_fp)
    return ocrout2result(out, cropped_pos1)


def number_predict(
    img_fp: Union[str, Path, Image.Image, np.ndarray],
    cropped_pos1: Tuple[int, int] = (0, 0),
    cropped_pos2: Tuple[int, int] = (0, 0),
):
    """
    说明：
        OCR识别图片上的文字
    参数：
        :param img_fp: 图片
        :param cropped_pos: 切剪区域 (x1, x2, y1, y2)
    """
    if cropped_pos1 != (0, 0) and cropped_pos2 != (0, 0):
        img_fp = img_fp[
            cropped_pos1[1] : cropped_pos2[1], cropped_pos1[0] : cropped_pos2[0]
        ]
    out = number_ocr.ocr(img_fp)
    return ocrout2result(out, cropped_pos1)
