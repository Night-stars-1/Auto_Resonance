"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2024-04-03 13:45:03
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger

from core.adb import connect
from core.analysis_tasks import AnalysisTasks
from core.utils import read_json

if __name__ == "__main__":
    status = connect()
    if status:
        tasks = read_json("actions/start.json")
        for task in tasks:
            if isinstance(task, str):
                analysis = AnalysisTasks(task)
                analysis.start()
                logger.info(f"{task}运行完成")
            elif isinstance(task, dict):
                name = list(task.keys())[0]
                num = list(task.values())[0]
                for i in range(num):
                    analysis = AnalysisTasks(name)
                    analysis.start()
                    logger.info(f"{name}:{i+1}/{num}运行完成")
    else:
        logger.error("ADB连接失败")
