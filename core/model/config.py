"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 17:45:06
LastEditTime: 2024-04-21 02:07:53
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import json
from pathlib import Path
from typing import Dict, List

from loguru import logger
from pydantic import BaseModel, Field

ROOT_PATH = Path().resolve()
"""项目根目录路径"""
CONFIG_PATH = ROOT_PATH / "config" / "config.json"
"""自动程序配置文件路径"""
CONFIG_PATH.parent.exists() or CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)


class RestAreaModel(BaseModel):
    """休息区模型"""

    class RunTimeModel(BaseModel):
        runtime: float = 0.0
        """运行时间"""

    huashi: RunTimeModel = RunTimeModel()
    """桦石"""


class RSBModel(BaseModel):
    """铁安局模型"""

    city: str = "7号自由港"
    """刷取城市"""
    levelSerialPos: List[int] = [635, 662]
    """刷取关卡序号位置"""
    name: str = "所有"
    """刷取关卡名称 所有为全部刷取"""
    num: int = 1
    """刷取次数"""


class GlobalConfigModel(BaseModel):
    """全局配置模型"""

    is_speed: bool = True
    """是否使用加速弹丸"""
    is_auto_pick: bool = False
    """是否自动拾取"""


class Config(BaseModel):
    """自动程序配置"""

    version: str = "1.0.0"
    """版本号"""
    rsb: RSBModel = RSBModel()
    """铁安局配置"""
    rest_area: RestAreaModel = RestAreaModel()
    """休息区配置"""
    global_config: GlobalConfigModel = GlobalConfigModel()

    def save_config(self):
        """保存配置"""
        try:
            str_data = self.model_dump_json(indent=4, by_alias=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write(str_data)
        except (AttributeError, TypeError, ValueError, PermissionError):
            logger.exception(
                f"保存配置文件失败，请检查是否有权限读取和写入 {CONFIG_PATH}"
            )
            raise
        else:
            logger.info(f"配置文件 {CONFIG_PATH} 已保存。")


if CONFIG_PATH.exists() and CONFIG_PATH.is_file():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    config = Config.model_validate(data)
else:
    config = Config()
    try:
        str_data = config.model_dump_json(indent=4)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(str_data)
    except (AttributeError, TypeError, ValueError, PermissionError):
        logger.exception(f"创建配置文件失败，请检查是否有权限读取和写入 {CONFIG_PATH}")
        raise
    else:
        logger.info(f"配置文件 {CONFIG_PATH} 不存在，已创建默认插件配置文件。")
config.save_config()
