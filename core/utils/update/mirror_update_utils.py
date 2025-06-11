from typing import Callable

import requests
from loguru import logger

from core.utils.download_utils import download_file
from core.utils.update.base_update_utils import BaseUpdateUtils, LatestInfoResponse
from version import __version__

RES_ID = "Auto_Resonance"
LATEST_URL = f"https://mirrorchyan.com/api/resources/{RES_ID}/latest"


class MirrorUpdateUtils(BaseUpdateUtils):
    def get_latest_info(self, cdk: str):
        logger.info(f"获取最新版本信息 version={__version__} cdk={len(cdk)}")
        query = {"current_version": __version__, "cdk": cdk, "user_agent": RES_ID}
        resposne = requests.get(LATEST_URL, params=query)
        self.data = LatestInfoResponse.model_validate(resposne.json())
        return self.data
