# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """Signal bus"""

    switchToSampleCard = pyqtSignal(str, int)
    switchToCard = pyqtSignal(str)
    micaEnableChanged = pyqtSignal(bool)
    supportSignal = pyqtSignal()
    skillchanged = pyqtSignal()


signalBus = SignalBus()
