"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-07-09 13:16:26
LastEditTime: 2024-07-09 17:58:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import os.path
import time
import xml.etree.ElementTree as ET

import psutil
from loguru import logger

from core.model import app
from core.model.emulator import emulator_list


def strip_namespace(element: ET.Element):
    """
    用于忽略命名空间的函数
    """
    for elem in element.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]
    return element


def get_adb_by_VMS_path(path: str, key: str):
    tree = ET.parse(path)
    root = tree.getroot()

    root = strip_namespace(root)
    # 查找并打印ADB的hostport
    for forwarding in root.findall(".//NAT/Forwarding"):
        if forwarding.get("name") == key:
            hostport = forwarding.get("hostport")
            return hostport
    return ""


def get_adb_port():
    if app.Global.emulatorType == "Custom":
        return app.Global.adbPort, "自定义ADB端口"
    time.sleep(1.0)
    logger.info("开始获取ADB端口")
    for p in psutil.process_iter():
        try:
            exe_path = p.exe()
            exe_dir = os.path.dirname(exe_path)
            for emulator_data in emulator_list.root:
                if (
                    emulator_data.path in exe_path
                    and (
                        emulator_data.type == app.Global.emulatorType
                        or app.Global.emulatorType == "Auto"
                    )
                    and emulator_data.path != ""
                ):
                    adb_port = get_adb_by_VMS_path(
                        f"{exe_dir}\{emulator_data.VMS_path}",
                        emulator_data.adb_key,
                    )
                    return adb_port, emulator_data.name
        except (PermissionError, psutil.AccessDenied):
            pass
    return None, "未知"
