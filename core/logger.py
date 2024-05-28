"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2023-05-15 21:45:43
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2024-04-29 13:02:23
Description: 

Copyright (c) 2023 by Night-stars-1, All Rights Reserved. 
"""

import os.path
import sys

from loguru import logger

from version import __version__

path_log = os.path.join("logs", "debug.log")
LEVEL = "DEBUG"
logger.remove()

if not getattr(sys, "frozen", False):
    logger.add(
        sys.stdout,
        level=LEVEL,
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

logger.info(f"当前版本: {__version__}")
