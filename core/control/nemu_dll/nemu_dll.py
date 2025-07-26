import ctypes
import os

def init(path: str) -> ctypes.CDLL:
    global nemu
    if not os.path.exists(path):
        raise FileNotFoundError("文件不存在: " + path)
    nemu = ctypes.CDLL(path)
    return nemu
