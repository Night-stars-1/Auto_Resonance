from qfluentwidgets import IndeterminateProgressRing, PushSettingCard


class PrimaryPushLoadCard(PushSettingCard):

    def __init__(self, text, icon, title, content=None, parent=None):
        super().__init__(text, icon, title, content, parent)
        self.text = text
        self.spinner = IndeterminateProgressRing(self.button)
        self.spinner.setStrokeWidth(2)
        self.spinner.setFixedSize(24, 24)
        self.centerProgressRing()
        self.spinner.hide()

        self.button.setObjectName("PrimaryPushLoadCard")

    def centerProgressRing(self):
        # 计算进度环在按钮中的居中位置
        ring_size = self.spinner.size()
        button_size = self.button.size()
        new_x = (button_size.width() - ring_size.width()) // 2
        new_y = (button_size.height() - ring_size.height()) // 2
        self.spinner.move(new_x + 5, new_y)

    def loading(self, loading=True):
        if loading:
            self.spinner.show()
            self.button.setText("")
        else:
            self.spinner.hide()
            self.button.setText(self.text)
