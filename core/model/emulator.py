"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-07-09 14:32:22
LastEditTime: 2024-07-09 14:49:15
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import List

from pydantic import BaseModel, RootModel

{
    "name": "逍遥模拟器",
    "type": "MEnu",
    "path": "Microvirt\MEmu\MEmu.exe",
    "VMS_path": "MemuHyperv VMs\MEmu\MEmu.memu",
    "adb_key": "ADB",
}


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
