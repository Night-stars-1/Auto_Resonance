"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2023-05-15 21:45:43
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-07-17 23:26:54
Description: 

Copyright (c) 2023 by Night-stars-1, All Rights Reserved. 
"""

import os
import sys

from loguru import logger

path_log = os.path.join("logs", "debug.log")
level = "DEBUG"
logger.remove()

logger.add(
    sys.stdout,
    level=level,
    colorize=True,
    format="<cyan>{module}</cyan>.<cyan>{function}</cyan>"
    ":<cyan>{line}</cyan> - "
    "<level>{message}</level>",
)
logger.add(
    path_log,
    format="{time:HH:mm:ss} - "
    "{level}\t| "
    "{module}.{function}:{line} - "
    " {message}",
    rotation="1 days",
    enqueue=True,
    serialize=False,
    encoding="utf-8",
    retention="10 days",
)
