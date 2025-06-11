"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:30:29
LastEditTime: 2024-04-29 19:35:18
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
import json

from os import PathLike

from pathlib import Path

StrPath = str | PathLike[str]

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
RESOURCES_PATH = ROOT_PATH / "resources"
"""资源路径"""
TEMP_PATH = ROOT_PATH / "temp"
"""临时路径，用于存放下载的文件"""
TEMP_PATH.mkdir(exist_ok=True)

def read_json(path: StrPath):
    """
    读取 JSON 文件
    :param path: JSON 文件路径
    :return: JSON 数据
    """
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解码错误: {e}")
