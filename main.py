"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2024-05-19 21:26:03
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

import traceback
from pathlib import Path
from typing import Dict

from loguru import logger

import auto
from auto.run_business import stop as business_stop
from core.adb import connect
from core.adb import stop as adb_stop
from core.analysis_tasks import AnalysisTasks
from core.utils import read_json

analysis = None

NEW_UPDATER_PATH = Path("HeiYue Updater.exe.new")
OLD_UPDATER_PATH = Path("HeiYue Updater.exe")

# 检查是否存在HeiYue Updater.exe.new存在则覆盖HeiYue Updater.exe
if NEW_UPDATER_PATH.exists():
    NEW_UPDATER_PATH.replace(OLD_UPDATER_PATH)


def stop():
    """
    说明:
        停止运行
    """
    adb_stop()
    business_stop()


def main(tasks: Dict[str, str]):
    status = connect()
    if status:
        for description, task in tasks.items():
            logger.info(f"开始运行{description}")
            if task := getattr(auto, task, None):
                if start := getattr(task, "start"):
                    start()
                else:
                    logger.error(f"{task}模块没有start函数")
            else:
                logger.error(f"未找到{task}模块")
    else:
        logger.error("ADB连接失败")
    return status


def run():
    """
    这是从json文件中读取任务并执行的函数，可以根据需要修改json文件中的任务\n
    gui不会执行这个函数，如果需要执行这个函数，请执行main.py\n
    `python main.py`
    """
    global analysis
    status = connect()
    if status:
        tasks = read_json("actions/start.json")
        for task in tasks:
            if isinstance(task, str):
                analysis = AnalysisTasks(task)
                if (status := analysis.start()) == False:
                    return
                logger.info(f"{task}运行完成")
            elif isinstance(task, dict):
                name = list(task.keys())[0]
                num = list(task.values())[0]
                for i in range(num):
                    analysis = AnalysisTasks(name)
                    if (status := analysis.start()) == False:
                        return
                    logger.info(f"{name}:{i+1}/{num}运行完成")
    else:
        logger.error("ADB连接失败")


if __name__ == "__main__":
    run()
