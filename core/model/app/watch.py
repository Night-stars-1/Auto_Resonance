"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-05-07 00:05:56
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2025-02-05 18:48:52
"""

import json
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from core.model.app.index import APP_PATH, Config, app


class FileHandler(FileSystemEventHandler):
    """监听文本改动"""

    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path

    @property
    def get_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def on_modified(self, event):
        if not event.is_directory and event.src_path == str(self.file_path):
            _app = Config.model_validate(self.get_data)
            for attr_name in app.__dict__.keys():
                setattr(app, attr_name, getattr(_app, attr_name))

# 创建文件系统事件处理器
event_handler = FileHandler(APP_PATH)

# 创建观察者对象
observer = Observer()
observer.schedule(event_handler, path=APP_PATH.parent, recursive=False)

# 启动观察者
observer.start()
