from loguru import logger
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel

from app.common.worker import Worker
from core.utils.update.mirror_update_utils import MirrorUpdateUtils, LatestInfoResponse

class UpdateMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('检测更新中', self)
        self.bodyLabel = BodyLabel(self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.bodyLabel)

        self.yesButton.setText("更新")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(350)

    def update_title(self, title: str):
        self.titleLabel.setText(title)

    def show(self):
        super().show()
        self.worker = Worker(MirrorUpdateUtils().get_latest_info, cdk="")
        self.worker.result.connect(self.show_release_note)
        self.worker.start()

    def show_release_note(self, result: LatestInfoResponse):
        self.bodyLabel.setText(result.data.release_note)
        logger.info(result)


class UpdateProgressBar(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('更新', self)
        self.progressBar = ProgressBar(self)
        self.progressBar.setRange(0, 100)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progressBar)

        self.yesButton.hide()
        self.cancelButton.hide()
        self.buttonGroup.setVisible(False)

        self.widget.setMinimumWidth(350)

    def update_title(self, title: str):
        self.titleLabel.setText(title)
    
    def set_progress(self, value: int):
        self.progressBar.setValue(value)
