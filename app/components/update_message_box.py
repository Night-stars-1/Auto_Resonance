from loguru import logger
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel

import subprocess
from app.common.worker import UpdateWorker, Worker
from core.utils.update.base_update_utils import BaseUpdateUtils
from core.utils.update.mirror_update_utils import MirrorUpdateUtils, LatestInfoResponse


class UpdateMessageBox(MessageBoxBase):
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
        update_utils = MirrorUpdateUtils()
        self.updateProgress = UnzipProgressBar(update_utils, parent=self.parent())

        self.worker = Worker(update_utils.get_latest_info, cdk=cdk)
        self.worker.result.connect(self.show_release_note)
        self.worker.start()

    def show_release_note(self, result: LatestInfoResponse):

        self.bodyLabel.setText(result.data.release_note)
        logger.debug(result)

        # 绑定下载事件
        self.yesButton.clicked.connect(self.update)
        self.yesButton.setEnabled(True)

    def update(self):
        subprocess.Popen(
            ["HeiYue Updater.exe"], creationflags=subprocess.DETACHED_PROCESS
        )
        exit()


class UpdateProgressBar(MessageBoxBase):
    """更新进度条对话框"""

    def __init__(self, update_utils: BaseUpdateUtils, parent=None):
        super().__init__(parent)
        self.update_utils = update_utils

        self.titleLabel = SubtitleLabel("下载更新中...", self)
        self.progressBar = ProgressBar(self)
        self.progressBar.setRange(0, 100)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progressBar)

        self.yesButton.hide()
        self.cancelButton.hide()
        self.buttonGroup.setVisible(False)

        self.widget.setMinimumWidth(350)

    def show(self):
        super().show()
        self.worker = UpdateWorker(self.update_utils.download)
        self.worker.progress_changed.connect(self.set_progress)
        self.worker.update_finished.connect(self.update_finished)
        self.worker.start()

    def update_title(self, title: str):
        self.titleLabel.setText(title)

    def set_progress(self, value: int):
        self.progressBar.setValue(value)

    def update_finished(self, success: bool):
        logger.info(f"下载完成: {success}")
        if success:
            self.update_title("下载完成")
            self.set_progress(100)

            # 解压
            UnzipProgressBar(self.update_utils, parent=self.parent()).show()
        else:
            self.update_title("下载失败")
            self.set_progress(0)
        self.close()


class UnzipProgressBar(MessageBoxBase):
    """解压更新包进度条对话框"""

    def __init__(self, update_utils: BaseUpdateUtils, parent=None):
        super().__init__(parent)
        self.update_utils = update_utils

        self.titleLabel = SubtitleLabel("解压更新中...", self)
        self.progressBar = ProgressBar(self)
        self.progressBar.setRange(0, 100)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progressBar)

        self.yesButton.hide()
        self.cancelButton.hide()
        self.buttonGroup.setVisible(False)

        self.widget.setMinimumWidth(350)

    def show(self):
        super().show()
        self.worker = UpdateWorker(self.update_utils.unzip)
        self.worker.progress_changed.connect(self.set_progress)
        self.worker.update_finished.connect(self.update_finished)
        self.worker.start()

    def update_title(self, title: str):
        self.titleLabel.setText(title)

    def set_progress(self, value: int):
        self.progressBar.setValue(value)

    def update_finished(self, success: bool):
        logger.info(f"解压完成: {success}")
        if success:
            self.update_title("更新完成")
            self.set_progress(100)
        else:
            self.update_title("更新失败")
            self.set_progress(0)
        # self.close()
