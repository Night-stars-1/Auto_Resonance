"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:29:48
LastEditTime: 2024-04-08 21:33:26
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import QThread
from core.exceptions import StopExecution

class Worker(QThread):
    def __init__(self, func, stop, parent=None):
        super(Worker, self).__init__(parent)
        self.func = func
        self.stop_func = stop

    def run(self):
        try:
            self.func()
        except StopExecution:
            pass

    def stop(self):
        self.stop_func()
