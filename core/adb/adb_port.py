"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-07-09 13:16:26
LastEditTime: 2025-02-05 18:05:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
import xml.etree.ElementTree as ET
from os import path

import psutil
import win32gui
import win32process
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


def get_pid2title():
    pid2title = {}

    def enum_windows_callback(hwnd, lparam):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        window_title = win32gui.GetWindowText(hwnd)
        if found_pid not in pid2title or "模拟器" in window_title:
            pid2title[found_pid] = window_title
        return True

    win32gui.EnumWindows(enum_windows_callback, None)
    return pid2title


def get_all_port():
    """
    获取所有模拟器ADB端口信息
    """
    time.sleep(1)
    data = {}
    pid2title = get_pid2title()
    emulator_names = emulator_list.exe_name2data.keys()
    for p in psutil.process_iter():
        ...
        # try:
        #     vms_path = ""
        #     exe_name = p.name()
        #     if exe_name in emulator_names:
        #         emulator_data = emulator_list.exe_name2data[exe_name]
        #         if (
        #             emulator_data.VMS_folder_path is None
        #             or emulator_data.VMS_file is None
        #         ):
        #             continue
        #         for open_file in p.open_files():
        #             folder_path = open_file.path.replace("\\", "/")
        #             if emulator_data.VMS_folder_path in folder_path:
        #                 folder_path_split = folder_path.split(
        #                     emulator_data.VMS_folder_path
        #                 )
        #                 vms_path = path.join(
        #                     folder_path_split[0],
        #                     emulator_data.VMS_folder_path
        #                     + folder_path_split[1].split("/")[0],
        #                     emulator_data.VMS_file,
        #                 )
        #                 vms_folder_name = path.basename(
        #                     emulator_data.VMS_folder_path
        #                     + folder_path_split[1].split("/")[0]
        #                 )
        #                 vms_path = vms_path.format(VMS_folder_name=vms_folder_name)
        #                 break
        #         else:
        #             continue
        #         adb_port = get_adb_by_VMS_path(vms_path, emulator_data.adb_key)
        #         title = pid2title[p.pid]
        #         data[title] = adb_port
        # except (PermissionError, psutil.AccessDenied, AttributeError):
        #     pass
    return data


def get_adb_port():
    if app.Global.emulatorType == "Custom":
        return app.Global.adbPort, "自定义ADB端口"
    time.sleep(1.0)
    logger.info("开始获取ADB端口")
    for p in psutil.process_iter():
        try:
            exe_path = p.exe()
            exe_dir = path.dirname(exe_path)
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
