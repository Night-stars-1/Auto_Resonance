"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:29:48
LastEditTime: 2024-04-12 00:59:07
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import QThread

from core.exceptions import StopExecution

from .config import cfg


class Worker(QThread):
    def __init__(self, func, stop, **kargs):
        super(Worker, self).__init__()
        self.func = func
        self.stop_func = stop
        self.kargs = kargs

    def run(self):
        try:
            self.func(**self.kargs)
        except StopExecution:
            pass

    def stop(self):
        self.stop_func()
