"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:25:55
LastEditTime: 2024-04-02 18:39:41
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
            action["image"] = "resources/" + action.get("image", "")
            match action["type"]:
                case "wait":
                    self.wait(
                        action["image"],
                        action.get("cropped_pos", (0, 0, 0, 0)),
                        action.get("trynum", 10),
                    )
                case "click_image":
                    self.click_image(action["image"], action.get("cropped_pos", (0, 0, 0, 0)))
                case "click":
                    self.click(action["pos"])
                case "ocr_click":
                    self.ocr_click(
                        action["text"], action.get("cropped_pos", (0, 0, 0, 0))
                    )
                case _:
                    raise ValueError(f"Unknown action {action}")

    def wait(
        self,
        image_path: str,
        cropped_pos: Tuple[int, int, int, int] = (0, 0, 0, 0),
        trynum=10,
    ):
        for _ in range(trynum):
            image = screenshot()
            result = match_screenshot(image, image_path, cropped_pos)
            if result["max_val"] > 0.95:
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
