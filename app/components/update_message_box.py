from typing import Optional

from loguru import logger
from qfluentwidgets import BodyLabel, MessageBoxBase, ProgressBar, SubtitleLabel

from app.common.worker import UpdateWorker, Worker
from core.utils.update.base_update_utils import BaseUpdateUtils, UpdateStatus
from core.utils.update.mirror_update_utils import LatestInfoResponse, MirrorUpdateUtils


class UpdateMessageBox(MessageBoxBase):
    update_utils: MirrorUpdateUtils

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
    
    def update_body(self, body: str):
        self.bodyLabel.setText(body)

    def show(self, cdk: str, data: Optional[LatestInfoResponse] = None):
        super().show()
        self.update_utils = MirrorUpdateUtils()
        if data:
            self.update_utils.data = data
        
        self.updateProgress = UpdateProgressBar(self.update_utils, parent=self.parent())

        self.worker = Worker(
            self.update_utils.get_update_status, cdk=cdk
        )
        self.worker.result.connect(self.show_release_note)
        self.worker.start()

    def show_release_note(self, status: UpdateStatus):
        if status == UpdateStatus.LATEST:
            self.update_title("检查更新成功")
            self.update_body("当前已是最新版本")
            self.yesButton.hide()
            self.cancelButton.setText("关闭")
            return
        elif status == UpdateStatus.UPDATE:
            logger.debug(self.update_utils.data)
            self.bodyLabel.setText(self.update_utils.data.data.release_note)

            # 绑定下载事件
            self.yesButton.clicked.connect(self.download)
            self.yesButton.setEnabled(True)
        elif status == UpdateStatus.FAILDCDK:
            self.update_title("检查更新失败")
            self.bodyLabel.setText("Mirror CDK无效")
            self.yesButton.hide()
            self.cancelButton.setText("关闭")
            return
        else:
            self.update_title("检查更新失败")
            self.bodyLabel.setText("请稍后再试或联系开发者。")
            self.yesButton.hide()
            self.cancelButton.setText("关闭")

    def download(self):
        self.hide()
        self.updateProgress.show()


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
            self.update_title("解压完成")
            self.set_progress(100)

            # 移动文件
            MoveFileProgressBar(self.update_utils, parent=self.parent()).show()
        else:
            self.update_title("解压失败")
            self.set_progress(0)
        self.close()

class MoveFileProgressBar(MessageBoxBase):
    """解压更新包进度条对话框"""

    def __init__(self, update_utils: BaseUpdateUtils, parent=None):
        super().__init__(parent)
        self.update_utils = update_utils

        self.titleLabel = SubtitleLabel("移动文件中...", self)
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
        self.worker = UpdateWorker(self.update_utils.move_file)
        self.worker.progress_changed.connect(self.set_progress)
        self.worker.update_finished.connect(self.update_finished)
        self.worker.start()

    def update_title(self, title: str):
        self.titleLabel.setText(title)

    def set_progress(self, value: int):
        self.progressBar.setValue(value)

    def update_finished(self, success: bool):
        logger.info(f"更新完成: {success}")
        if success:
            self.update_title("更新完成")
            self.set_progress(100)
        else:
            self.update_title("更新失败")
            self.set_progress(0)
        # self.close()
