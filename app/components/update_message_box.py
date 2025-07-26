from loguru import logger
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel

import subprocess
from app.utils.worker import UpdateWorker, Worker
from core.utils.update.base_update_utils import BaseUpdateUtils
from core.utils.update.mirror_update_utils import MirrorUpdateUtils, LatestInfoResponse


class UpdateMessageBox(MessageBoxBase):
    cdk: str = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("检测更新中", self)
        self.bodyLabel = BodyLabel(self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.bodyLabel)

        self.yesButton.setText("更新")
        self.yesButton.setEnabled(False)
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(350)

    def update_title(self, title: str):
        self.titleLabel.setText(title)

    def show(self, cdk: str):
        super().show()
        self.cdk = cdk

        update_utils = MirrorUpdateUtils()

        self.worker = Worker(update_utils.get_latest_info, cdk=cdk)
        self.worker.result.connect(self.show_release_note)
        self.worker.start()

    def show_release_note(self, result: LatestInfoResponse):

        self.bodyLabel.setText(result.data.release_note)
        logger.debug(result)

        # 绑定下载事件
        self.yesButton.clicked.connect(lambda: self.update(result))
        self.yesButton.setEnabled(True)

    def update(self, data: LatestInfoResponse):
        subprocess.Popen(
            ["HeiYue Updater.exe", "--mirror_cdk", self.cdk, "--update_data", data.model_dump_json()],
            creationflags=subprocess.DETACHED_PROCESS,
        )
        exit()
