"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:29:48
LastEditTime: 2024-04-19 13:24:00
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
import inspect

from loguru import logger
from PyQt5.QtCore import QThread, pyqtSignal

from core.utils.update.base_update_utils import BaseUpdateUtils


class Worker(QThread):
    result = pyqtSignal(object)

    def __init__(self, func, stop = lambda : None, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.stop_func = stop
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(**self.kwargs)
            self.result.emit(result)
        except AssertionError as e:
            logger.error(f"{e}")
        except Exception:
            logger.exception("崩溃信息:")

    def stop(self):
        self.stop_func()

class UpdateWorker(QThread):
    progress_changed = pyqtSignal(int)
    update_finished = pyqtSignal(bool)

    def __init__(self, func, **kwargs):
        super(UpdateWorker, self).__init__()
        self.func = func
        self.kwargs = kwargs
        # 检查函数是否接受update_progress参数
        sig = inspect.signature(func)
        if "progress_changed" in sig.parameters and "progress_changed" not in kwargs:
            self.kwargs["progress_changed"] = self.progress_changed.emit
        if "update_finished" in sig.parameters and "update_finished" not in kwargs:
            self.kwargs["update_finished"] = self.update_finished.emit

    def run(self):
        try:
            self.func(**self.kwargs)
        except AssertionError as e:
            logger.error(f"{e}")
        except Exception:
            logger.exception("崩溃信息:")
