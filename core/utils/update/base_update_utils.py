from abc import ABC, abstractmethod

from typing import Optional
from pydantic import BaseModel

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
    @abstractmethod
    def get_latest_info(self):
        pass
