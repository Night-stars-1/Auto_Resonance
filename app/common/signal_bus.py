from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """Signal bus"""

    switchToCard = Signal(str)


signalBus = SignalBus()
