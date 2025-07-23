from typing import Optional, Union

import cv2 as cv
from loguru import logger
import numpy as np
from core.adb.adb_port import get_adb_port
from core.adb.base_control import IADB
from subprocess import DEVNULL, CompletedProcess
from subprocess import run as _run
from adb_shell.adb_device import AdbDeviceTcp

from core.model import app

PNG_KEY = b"\x89PNG"

def run(
    *popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs
) -> CompletedProcess:
    return _run(
        *popenargs,
        shell=True,
        input=input,
        capture_output=capture_output,
        timeout=timeout,
        check=check,
        **kwargs,
    )


class ADB(IADB):
    def __init__(self) -> None:
        super().__init__()
        self.adb_path = app.Global.adbPath
        self.adb_host = "127.0.0.1"
        self.device = AdbDeviceTcp(self.adb_host)

    def connect(self, adb_port: Optional[int] = None) -> bool:
        name = "自定义ADB端口"
        if adb_port is None:
            adb_port, name = get_adb_port()
        if adb_port is None:
            logger.info(f"未知ADB端口信息 {name}，请检测ADB端口是否设置正确")
            return False
        logger.info(f"ADB端口：{name}-{adb_port}")
        self.device = AdbDeviceTcp(self.adb_host, port=adb_port)
        try:
            status = self.device.connect()
            if not status:
                logger.error("ADB连接失败")
        except ConnectionRefusedError:
            status = False
            logger.error("ADB端口错误或者未打开模拟器，无法连接")
        return status

    def input_swipe(self, x1: int, y1: int, x2: int, y2: int, time: int = 100) -> None:
        shell = [
            "input",
            "swipe",
            f"{x1} {y1} {x2} {y2}",
            f"{time}",
        ]
        self.device.shell(" ".join(shell))

    def input_tap(self, x: int, y: int):
        shell = [
            "input",
            "tap",
            str(x),
            str(y),
        ]
        self.device.shell(" ".join(shell))

    def screenshot(self) -> cv.typing.MatLike:
        screenshot_data = self.device.shell("screencap -p", decode=False)
        if isinstance(screenshot_data, str):
            raise Exception(f"无法获取屏幕截图: {screenshot_data}")
        if screenshot_data[:4] != PNG_KEY:
            index = screenshot_data.find(PNG_KEY)
            if index == -1:
                raise Exception("无法获取屏幕截图: 截图数据不包含PNG头")
            screenshot_data = screenshot_data[index:]
            logger.debug(f"screenshot: {screenshot_data[:10]}...")

        image_array = np.frombuffer(screenshot_data, np.uint8)

        screenshot = cv.imdecode(image_array, cv.IMREAD_COLOR)

        return screenshot

    def kill(self):
        """
        说明:
            关闭ADB
        """
        self.device.close()
