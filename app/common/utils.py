"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-06 21:18:58
LastEditTime: 2024-04-06 21:19:14
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""
import json
import threading
from functools import wraps
from typing import Union


def debounce(wait):
    """
    说明:
        防抖装饰器：等待指定时间后执行函数，如果在等待时间内再次触发，则重新计时
    """
    def decorator(fn):
        @wraps(fn)
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            if hasattr(debounced, '_timer'):
                debounced._timer.cancel()
            debounced._timer = threading.Timer(wait, call_it)
            debounced._timer.start()
        return debounced
    return decorator

def save_json(path: str, data: Union[dict, list]):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_json(path: str, default: Union[dict, list] = {}) -> Union[dict, list]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default
    except FileNotFoundError:
        return default
