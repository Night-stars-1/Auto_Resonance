"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 20:11:21
LastEditTime: 2024-04-08 21:39:12
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from functools import wraps
from typing import Callable


# 定义装饰器
def ensure_resources_prefix(func: Callable) -> Callable:
    """
    说明:
        确保传入的图片路径有前缀'resources/'
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_list = list(args)
        if args and not args[0].startswith("resources"):
            arg_list[0] = "resources/" + args[0]
        args = tuple(arg_list)

        if "image" in kwargs and not kwargs["image"].startswith("resources/"):
            kwargs["image"] = "resources/" + kwargs["image"]

        return func(*args, **kwargs)

    return wrapper
