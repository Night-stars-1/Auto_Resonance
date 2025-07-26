from abc import ABC, abstractmethod
from typing import Optional
import cv2 as cv
from loguru import logger

class IADB(ABC):
    dsize = (1280, 720)
    ratio = 1
    safe_area = (0, 0, 1280, 720)

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def connect(self, adb_port: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def input_swipe(self, x1: int, y1: int, x2: int, y2: int, time: int = 100) -> None:
        pass

    @abstractmethod
    def input_tap(self, x: int, y: int):
        pass

    @abstractmethod
    def screenshot(self) -> cv.typing.MatLike:
        pass
    
    @abstractmethod
    def kill(self):
        pass
    
    def check_resolution_ratio(self, width: int, height: int) -> bool:
        """检查分辨率比例是否符合要求"""
        if width <= 0 or height <= 0:
            return False
        ratio = width / height
        checked = ratio == 16 / 9
        self.ratio = width / self.dsize[0]
        self.safe_area = (int(self.ratio * 20), int(self.ratio * 70), int(self.ratio * 1200), int(self.ratio * 700))
        if not checked:
            logger.error(f"分辨率必须为16:9 (实际比例: {ratio:.2f})")
        return checked
