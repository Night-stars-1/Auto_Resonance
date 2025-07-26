import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

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

    def get_update_status(self, cdk: str, reload: bool = False) -> UpdateStatus:
        """
        获取更新状态
        :return: 更新状态
        """
        if not getattr(sys, "frozen", False):
            return UpdateStatus.NOSUPPORT
        if not self.data or reload:
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
