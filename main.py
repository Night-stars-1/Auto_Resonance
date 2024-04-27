"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-03-20 22:24:35
LastEditTime: 2024-04-27 14:54:08
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger

from auto.huashi.main import start as ra_start
from auto.railway_safety_bureau.main import start as rsb_start
from core.adb import connect
from core.adb import stop as adb_stop
from core.analysis_tasks import AnalysisTasks
from core.utils import read_json

analysis = None


def stop():
    """
    说明:
        停止运行
    """
    adb_stop()


def main(order, path):
    status = connect(order, path)
    if status:
        ra_start()
        rsb_start()
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
