"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2024-04-02 17:42:25
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
            analysis = AnalysisTasks(task)
            analysis.start()
    else:
        logger.error("ADB连接失败")
