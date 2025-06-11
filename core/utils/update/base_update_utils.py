import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional

from loguru import logger
from pydantic import BaseModel

from core.utils.download_utils import download_file, unzip
from core.utils.utils import TEMP_PATH


class UpdateStatus(Enum):
    """更新状态枚举类"""

    LATEST = 1
    UPDATE = 2
    FAILED = 0
    NOSUPPORT = 3
    FAILDCDK = 4


class Data(BaseModel):
    """响应数据"""

    """更新包架构"""
    arch: str
    """更新频道，stable | beta | alpha"""
    channel: str
    """更新包系统"""
    os: str
    """发版日志"""
    release_note: str
    """资源版本名称"""
    version_name: str
    """资源版本号仅内部使用"""
    version_number: int
    """CDK过期时间戳"""
    cdk_expired_time: Optional[float] = None
    """自定义数据"""
    custom_data: Optional[str] = None
    """文件大小"""
    filesize: Optional[int] = None
    """sha256"""
    sha256: Optional[str] = None
    """更新包类型，incremental | full"""
    update_type: Optional[str] = None
    """下载地址"""
    url: Optional[str] = None


class LatestInfoResponse(BaseModel):
    """响应代码，https://github.com/MirrorChyan/docs/blob/main/ErrorCode.md"""

    code: int
    """响应信息"""
    msg: str
    """响应数据"""
    data: Optional[Data] = None


class BaseUpdateUtils(ABC):
    zip_name = "Auto_Resonance.zip"
    zip_path = TEMP_PATH / zip_name
    data: LatestInfoResponse = None

    @abstractmethod
    def get_latest_info(self, cdk: str) -> LatestInfoResponse:
        pass

    def download(
        self,
        progress_changed: Callable[[int], None],
        update_finished: Callable[[bool], None],
    ):
        if not self.data:
            raise ValueError("data未初始化，请先调用get_latest_info")
        if self.data.code != 0:
            raise ValueError(f"获取最新信息失败: {self.data.msg}")
        download_url = self.data.data.url
        update_type = self.data.data.update_type
        logger.info(f"开始下载更新包: {update_type}-{download_url}")
        if not download_url:
            raise ValueError("下载地址未空")
        download_file(
            url=download_url,
            path=self.zip_path,
            progress_changed=progress_changed,
            update_finished=update_finished,
        )
        logger.info(f"更新包下载完成: {self.zip_name}")

    def unzip(
        self,
        progress_changed: Optional[Callable[[int], None]] = None,
        update_finished: Optional[Callable[[bool], None]] = None,
    ):
        """
        解压更新包
        :param progress_changed: 可选的进度更新回调函数，接收一个整数参数表示解压进度百分比
        :param update_finished: 可选的更新完成回调函数，接收一个布尔值表示是否成功
        """
        logger.info(f"开始解压更新包: {self.zip_name}")
        if not self.zip_path.exists():
            raise FileNotFoundError(f"更新包不存在: {self.zip_path}")
        unzip(
            zip_path=self.zip_path,
            extract_path=TEMP_PATH / "Auto_Resonance",
            progress_changed=progress_changed,
            update_finished=update_finished,
        )

        logger.info(f"更新包解压完成: {self.zip_name}")

    def get_update_status(self, cdk: str) -> UpdateStatus:
        """
        获取更新状态
        :return: 更新状态
        """
        if not getattr(sys, "frozen", False):
            return UpdateStatus.NOSUPPORT
        if not self.data:
            self.data = self.get_latest_info(cdk=cdk)
        if not self.data:
            return UpdateStatus.FAILED
        elif self.data.code == 7002:
            return UpdateStatus.FAILDCDK
        elif self.data.code != 0:
            return UpdateStatus.FAILED
        elif self.data.msg == "current version is latest":
            return UpdateStatus.LATEST
        elif self.data.data.url:
            return UpdateStatus.UPDATE
        else:
            return UpdateStatus.FAILED
