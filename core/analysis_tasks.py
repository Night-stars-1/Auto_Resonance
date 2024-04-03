"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:25:55
LastEditTime: 2024-04-03 13:17:37
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Dict, List, Optional, Tuple

from loguru import logger

from .adb import input_tap, screenshot
from .image import match_screenshot, show_image
from .ocr import predict
from .utils import read_json


class AnalysisTasks:
    def __init__(self, task_name):
        self.task_name = task_name
        self.actions: List[Dict[str, str]] = read_json(
            f"actions/tasks/{task_name}.json"
        )

    def start(self):
        for action in self.actions:
            if "image" in action:
                action["image_path"] = "resources/" + action.pop("image", "")
            action_type = action.pop("type")
            method = getattr(self, action_type, None)
            try:
                if method:
                    method(**action)
                else:
                    raise ValueError(f"未知活动 {action}")
            except TypeError as error:
                error_str = str(error)
                if (
                    "required positional argument" in error_str
                    or "required keyword-only argument" in error_str
                ):
                    missing_arg = error_str.split("argument: ")[-1].replace("'", "")
                    action_data = {"type": action_type, **action}
                    logger.error(f"{action_data} - 错误：缺少必需的参数 - {missing_arg}")
                elif (
                    "got an unexpected keyword argument" in error_str
                ):
                    missing_arg = error_str.split("argument")[-1].replace("'", "")
                    action_data = {"type": action_type, **action}
                    logger.error(f"{action_data} - 错误：多余的参数 - {missing_arg}")
                else:
                    logger.error(error)

    def wait(
        self,
        image_path: str,
        cropped_pos: Tuple[int, int, int, int] = (0, 0, 0, 0),
        trynum=10,
        threshold = 0.95
    ):
        for _ in range(trynum):
            image = screenshot()
            result = match_screenshot(image, image_path, cropped_pos)
            if result["max_val"] >= threshold:
                break
            time.sleep(1)

    def click_image(self, image_path: str, cropped_pos: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        image = screenshot()
        result = match_screenshot(image, image_path, cropped_pos)
        if result["max_val"] > 0.95:
            pos = result["max_loc"]
            input_tap(pos)
        else:
            logger.error(f"未找到指定图片 => {image_path}")

    def click(self, pos):
        input_tap(pos)

    def ocr_click(
        self, text: str, cropped_pos: Tuple[int, int, int, int] = (0, 0, 0, 0)
    ):
        image = screenshot()
        data = predict(image, cropped_pos)
        coordinates = None
        for item in data:
            if item["text"] == text:
                # 读取位置信息
                position = item["position"]
                # 计算中心坐标
                center_x = (position[0][0] + position[2][0]) / 2
                center_y = (position[0][1] + position[2][1]) / 2
                coordinates = (center_x, center_y)
                break
        if coordinates:
            input_tap(coordinates)
        else:
            logger.error(f"未找到指定文本 => {text}")
