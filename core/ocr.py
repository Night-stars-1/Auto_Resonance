"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 21:40:57
LastEditTime: 2024-04-03 20:24:24
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
from cnocr import CnOcr
from PIL import Image

ocr = CnOcr()


def predict(
    img_fp: Union[str, Path, Image.Image, np.ndarray],
    cropped_pos: Optional[Tuple[int, int, int, int]] = (0, 0, 0, 0),
):
    """
    说明：
        OCR识别图片上的文字
    参数：
        :param img_fp: 图片
        :param cropped_pos: 切剪区域 (x1, x2, y1, y2)
    """
    if cropped_pos != (0, 0, 0, 0):
        img_fp = img_fp[
            cropped_pos[2] : cropped_pos[3], cropped_pos[0] : cropped_pos[1]
        ]
    out = ocr.ocr(img_fp)
    return [
        {
            "text": predict_data["text"],
            "score": predict_data["score"],
            "position": [
                [
                    predict_data["position"][0][0] + cropped_pos[0],
                    predict_data["position"][0][1] + cropped_pos[2],
                ],
                [
                    predict_data["position"][1][0] + cropped_pos[0],
                    predict_data["position"][1][1] + cropped_pos[2],
                ],
                [
                    predict_data["position"][2][0] + cropped_pos[0],
                    predict_data["position"][2][1] + cropped_pos[2],
                ],
                [
                    predict_data["position"][3][0] + cropped_pos[0],
                    predict_data["position"][3][1] + cropped_pos[2],
                ],
            ],
        }
        for predict_data in out
    ]
