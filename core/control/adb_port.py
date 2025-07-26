"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-07-09 13:16:26
LastEditTime: 2025-02-05 18:05:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
import time
from dataclasses import dataclass
from enum import Enum
from os import path
from subprocess import run

import psutil
from loguru import logger


class EmulatorType(Enum):
    MUMUV5 = "MuMuV5"
    CUSTOM = "Custom"


@dataclass
class EmulatorDataItem:
    name: str
    manager_path: str
    dir_path: str
    params: str
    type: EmulatorType


@dataclass
class EmulatorInfo:
    name: str
    port: int
    path: str
    type: EmulatorType
    index: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "port": self.port,
            "path": self.path,
            "type": self.type.value,
            "index": self.index,
        }

    @staticmethod
    def from_dict(data: dict) -> "EmulatorInfo":
        return EmulatorInfo(
            name=data["name"],
            port=data["port"],
            path=data["path"],
            type=EmulatorType(data["type"]),
            index=data.get("index", 0),
        )

EMULATOR_DATA = {
    "MuMuNxDevice.exe": EmulatorDataItem(
        name="MuMu模拟器 V5",
        manager_path="../../../../nx_main/MuMuManager.exe",
        dir_path="../../../../",
        params="info -v all",
        type=EmulatorType.MUMUV5,
    )
}


def get_mumu_info(exe_path: str, data: EmulatorDataItem):
    """获取MuMu模拟器信息"""
    cmd_path = path.abspath(path.join(exe_path, data.manager_path))
    cmd = [cmd_path] + data.params.split()
    result = run(cmd, shell=False, capture_output=True, text=False)
    if result.returncode != 0:
        return []

    out = result.stdout
    result = json.loads(out)
    return [
        EmulatorInfo(
            name=i["name"],
            port=i.get("adb_port"),
            path=path.abspath(path.join(exe_path, data.dir_path)),
            type=data.type,
            index=int(i.get("index", "0"))
        )
        for i in result.values()
    ]


def get_emulator_info(exe_path: str, data: EmulatorDataItem):
    """获取模拟器信息"""
    if data.type == EmulatorType.MUMUV5:
        return get_mumu_info(exe_path, data)
    return []


def get_adb_port() -> list[EmulatorInfo]:
    time.sleep(1)
    logger.info("开始获取ADB端口")
    result = []
    for p in psutil.process_iter():
        try:
            exe_path = p.exe()
            exe_name = path.basename(exe_path)
            exe_data = EMULATOR_DATA.get(exe_name)
            if exe_data:
                info = get_emulator_info(exe_path, exe_data)
                result.extend(info)
        except (PermissionError, psutil.AccessDenied):
            pass
    return result
