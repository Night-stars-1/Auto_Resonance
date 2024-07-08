from PyQt5.QtWidgets import QVBoxLayout, QWidget

class BarCardView(QWidget):
    """Bar card view"""

    def __init__(self, widget: QWidget = None, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(36, 0, 0, 0)
        # self.vBoxLayout.setSpacing(10)

        self.vBoxLayout.addWidget(widget)
