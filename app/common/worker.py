"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 23:29:48
LastEditTime: 2024-04-06 23:29:57
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from PyQt5.QtCore import QThread


class Worker(QThread):
    def __init__(self, func, stop, parent=None):
        super(Worker, self).__init__(parent)
        self.func = func
        self.stop_func = stop

    def run(self):
        self.func()
    
    def stop(self):
        self.stop_func()

