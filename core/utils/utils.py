"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:30:29
LastEditTime: 2024-04-29 19:35:18
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from pathlib import Path
import sys
from typing import Any, List, Tuple, Union

ROOT_PATH = Path().resolve()
"""项目根目录"""
if getattr(sys, 'frozen', False):
    ROOT_PATH = Path(sys.executable).parent.resolve()
RESOURCES_PATH = ROOT_PATH / "resources"
"""资源路径"""
TEMP_PATH = ROOT_PATH / "temp"
"""临时路径，用于存放下载的文件"""

def save_json(path: str, data: Union[dict, list]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_json(path: Union[str, Path], default: Union[dict, list] = {}) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default
    except FileNotFoundError:
        return default

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
