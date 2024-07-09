"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-07-09 14:32:22
LastEditTime: 2024-07-09 16:08:11
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from functools import cached_property
from typing import List

from pydantic import BaseModel, RootModel

from core.utils import RESOURCES_PATH, read_json

emulator_list_json = read_json(RESOURCES_PATH / "adb" / "EmulatorData.json")


class EmulatorModel(BaseModel):
    """模拟器配置模型"""

    name: str
    """模拟器名称"""
    type: str
    """类型"""
    path: str
    """路径"""
    VMS_path: str
    """模拟器配置路径"""
    adb_key: str


class EmulatorListModel(RootModel):
    """模拟器列表模型"""

    root: List[EmulatorModel]

    @cached_property
    def name2type(self):
        return {i.name: i.type for i in self.root}

emulator_list = EmulatorListModel.model_validate(emulator_list_json)
