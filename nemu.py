import ctypes
import os

folder_path = "C:/Program Files/Netease/MuMuPlayer-12.0"
nemu = ctypes.CDLL(os.path.join(folder_path, "./shell/sdk/external_renderer_ipc.dll"))
