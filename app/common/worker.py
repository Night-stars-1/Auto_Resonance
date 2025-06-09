"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:29:48
LastEditTime: 2024-04-19 13:24:00
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import QThread, pyqtSignal
from loguru import logger

from core.exceptions import StopExecution

from .config import cfg


class Worker(QThread):
    result = pyqtSignal(object)

    def __init__(self, func, stop = lambda : None, **kargs):
        super(Worker, self).__init__()
        self.func = func
        self.stop_func = stop
        self.kargs = kargs

    def run(self):
        try:
            result = self.func(**self.kargs)
            self.result.emit(result)
        except StopExecution:
            pass
        except AssertionError as e:
            logger.error(f"{e}")
        except Exception:
            logger.exception("崩溃信息:")

    def stop(self):
        self.stop_func()

class UpdateWorker(Worker):
    progress_changed = pyqtSignal(int)
    update_finished = pyqtSignal(bool)

    def __init__(self, func, **kargs):
        super(UpdateWorker, self).__init__(func, lambda: None, **kargs)

