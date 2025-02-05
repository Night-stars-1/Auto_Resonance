"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-07-09 14:32:22
LastEditTime: 2025-02-05 18:00:41
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from functools import cached_property
from os import path
from typing import List, Optional

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
    VMS_folder_path: Optional[str] = None
    """模拟器VMS配置的文件夹"""
    VMS_path: str
    """模拟器配置路径"""
    VMS_file: Optional[str] = None
    """模拟器配置信息的文件名"""
    adb_key: str


class EmulatorListModel(RootModel):
    """模拟器列表模型"""

    root: List[EmulatorModel]

    @cached_property
    def name2type(self):
        return {i.name: i.type for i in self.root}
    
    @cached_property
    def exe_name2data(self):
        return {path.basename(i.path): i for i in self.root}
    
emulator_list = EmulatorListModel.model_validate(emulator_list_json)
