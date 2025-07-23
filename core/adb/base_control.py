from abc import ABC, abstractmethod
from typing import Optional
import cv2 as cv

class IADB(ABC):
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
    