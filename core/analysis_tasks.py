"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:25:55
LastEditTime: 2024-04-06 02:37:28
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Dict, List, Optional, Tuple

from loguru import logger

import core.presets

from .adb import input_tap, screenshot
from .ocr import predict
from .utils import read_json


class AnalysisTasks:
    def __init__(self, task_name):
        self.task_name = task_name
        self.actions: List[Dict[str, str]] = read_json(
            f"actions/tasks/{task_name}.json"
        )

    def start(self, actions=None):
        actions = actions or self.actions
        for action in actions:
            if "image" in action:
                action["image_path"] = "resources/" + action.pop("image", "")
            action_type = action.pop("type")
            method = getattr(core.presets, action_type, None)
            try:
                if method:
                    method(**action)
                elif action_type == "judgement_text":
                    self.judgement_text(**action)
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
                    logger.error(
                        f"{action_data} - 错误：缺少必需的参数 - {missing_arg}"
                    )
                elif "got an unexpected keyword argument" in error_str:
                    missing_arg = error_str.split("argument")[-1].replace("'", "")
                    action_data = {"type": action_type, **action}
                    logger.error(f"{action_data} - 错误：多余的参数 - {missing_arg}")
                else:
                    logger.error(error)

    def judgement_text(
        self,
        text: str,
        success: Optional[str | List[Dict[str, str]]],
        fail: Optional[str | List[Dict[str, str]]],
        cropped_pos1: Tuple[int, int] = (0, 0),
        cropped_pos2: Tuple[int, int] = (0, 0),
        must_succeed: bool = False,
        is_click: bool = False,
        is_use: bool = True,
    ):
        """
        说明:
            判断文本是否存在
        参数:
            :param text: 文本
            :param success: 成功操作
            :param fail: 失败操作
            :param cropped_pos1: 裁剪坐标1
            :param cropped_pos2: 裁剪坐标2
            :param must_succeed: 是否必须成功
            :param is_click: 是否点击
            :param is_use: 是否使用
        """
        if not is_use:
            return True
        logger.info(f"判断文本 {text} 是否存在")
        time.sleep(0.5)
        image = screenshot()
        data = predict(image, cropped_pos1, cropped_pos2)
        for item in data:
            if text in item["text"]:
                logger.info(f"找到文本 => {text}")
                if is_click:
                    position = item["position"]
                    # 计算中心坐标
                    center_x = (position[0][0] + position[2][0]) / 2
                    center_y = (position[0][1] + position[2][1]) / 2
                    input_tap((center_x, center_y))
                if isinstance(success, str):
                    actions = read_json(f"actions/actions/{success}.json")
                    self.start(actions)
                elif isinstance(success, list):
                    self.start(success)
                return
        logger.info(f"未找到文本 => {text}")
        if isinstance(fail, str):
            actions = read_json(f"actions/actions/{fail}.json")
            self.start(actions)
        elif isinstance(fail, list):
            self.start(fail)
        if not must_succeed:
            return
        else:
            self.judgement_text(
                text=text,
                success=success,
                fail=fail,
                cropped_pos1=cropped_pos1,
                cropped_pos2=cropped_pos2,
                must_succeed=must_succeed,
            )
