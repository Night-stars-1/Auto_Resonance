"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:30:29
LastEditTime: 2024-04-29 19:35:18
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from typing import List, Tuple, Union



def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compare_ranges(
    low: Union[Tuple[int, int, int], List[int]],
    x: Union[Tuple[int, int, int], List[int]],
    high: Union[Tuple[int, int, int], List[int]],
):
    """
    说明:
        判断指定颜色是否在范围
    参数:
        :param low: 最低颜色
        :param x: 目标颜色
        :param high: 最高颜色
    """
    # 解构列表到单独的变量
    low_0, low_1, low_2 = low
    x_0, x_1, x_2 = x
    high_0, high_1, high_2 = high

    # 比较每个元素
    return (
        (low_0 <= x_0 <= high_0)
        and (low_1 <= x_1 <= high_1)
        and (low_2 <= x_2 <= high_2)
    )
