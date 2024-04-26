"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-02 12:25:55
LastEditTime: 2024-04-08 20:14:10
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import time
from typing import Dict, List, Optional, Tuple, Union

from loguru import logger

import core.presets

from .presets import find_text
from .adb import input_tap, screenshot
from .ocr import predict
from .utils import read_json


class AnalysisTasks:
    def __init__(self, task_name):
        self.task_name = task_name
        self.actions: List[Dict[str, str]] = read_json(
            f"actions/tasks/{task_name}.json"
        )
        self.stop = False

    def start(self, actions=None):
        actions = actions or self.actions
        for action in actions:
            logger.debug(f"执行活动 => {action}")
            if self.stop:
                return False
            action_type = action.pop("type", "异常")
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
        success: Union[str, List[Dict[str, str]]],
        fail: Union[str, List[Dict[str, str]]],
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
        result = find_text(text, cropped_pos1, cropped_pos2)
        if result:
            action = success
            if is_click:
                input_tap(result["center"])
        else:
            action = fail
        if isinstance(fail, str):
            actions = read_json(f"actions/actions/{action}.json")
            self.start(actions)
        elif isinstance(action, list):
            self.start(action.copy())
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
