
import ctypes
import os
import time
from typing import Optional

from loguru import logger
import numpy as np
from core.control.adb_port import EmulatorType
from core.control.base_control import IADB
import cv2 as cv

from core.control.nemu_dll.nemu_dll import init
from core.model import app

def swipe_path(p0, p3, time):
    path = []
    p0 = np.array(p0)
    p3 = np.array(p3)
    p1 = 2/3 * p0 + 1/3 * p3
    p2 = 1/3 * p0 + 2/3 * p3

    time = int(time / 10)
    for i in range(time):
        t = i / (time - 1)

        point = (1 - t)**3 * p0 + \
            3 * (1 - t)**2 * t * p1 + \
            3 * (1 - t) * t**2 * p2 + \
            t**3 * p3
        point = point.astype(int).tolist()
        path.append(point)

    return path

class NEMU(IADB):
    def __init__(self) -> None:
        self.device = app.Global.device
        self.path = self.device.path
        if self.device.type == EmulatorType.MUMUV5:
            path = os.path.join(self.path, "./nx_device/12.0/shell/sdk/external_renderer_ipc.dll")
        elif self.device.type == EmulatorType.MUMUV4:
            path = os.path.join(self.path, "./shell/sdk/external_renderer_ipc.dll")
        else:
            raise Exception(f"不支持的模拟器类型: {self.device.type}")
        self.nemu = init(path)

    def connect(self, adb_port: Optional[int] = None) -> bool:
        logger.info("使用NEMUIPC连接")
        self.connect_id = self.nemu.nemu_connect(self.path, self.device.index)
        self.display_id = self.nemu.nemu_get_display_id(self.connect_id, b"com.hermes.goda", 0)

        # 获取尺寸
        self.width_ptr = ctypes.pointer(ctypes.c_int(0))
        self.height_ptr = ctypes.pointer(ctypes.c_int(0))
        nullptr = ctypes.POINTER(ctypes.c_ubyte)()
        self.nemu.nemu_capture_display(self.connect_id, self.display_id, 0, self.width_ptr, self.height_ptr, nullptr)

        self.width = self.width_ptr.contents.value
        self.height = self.height_ptr.contents.value

        self.length = self.width * self.height * 4
        self.pixels_array = (ctypes.c_ubyte * self.length)()
        self.pixels_pointer = ctypes.pointer(self.pixels_array)
        return self.check_resolution_ratio(self.width, self.height)

    def input_swipe(self, x1: int, y1: int, x2: int, y2: int, millisecond: int = 100) -> None:
        points = swipe_path((x1, y1), (x2, y2), millisecond)
        for point in points:
            self.nemu.nemu_input_event_touch_down(self.connect_id, self.display_id, *point)
            time.sleep(0.01)
        self.nemu.nemu_input_event_touch_up(self.connect_id, self.display_id)
        time.sleep(0.05)


    def input_tap(self, x: int, y: int):
        self.nemu.nemu_input_event_touch_down(self.connect_id, self.display_id, x, y)
        self.nemu.nemu_input_event_touch_up(self.connect_id, self.display_id)
        time.sleep(0.5)

    def screenshot(self) -> cv.typing.MatLike:
        self.nemu.nemu_capture_display(self.connect_id, self.display_id, self.length, self.width_ptr, self.height_ptr, self.pixels_pointer)
        image = np.frombuffer(self.pixels_array, dtype=np.uint8).reshape((self.height, self.width, 4))

        image = cv.cvtColor(image, cv.COLOR_BGRA2RGB)
        image = cv.flip(image, 0)
        return image
    
    def kill(self):
        pass
