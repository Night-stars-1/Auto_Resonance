import time
import requests
from core.utils.update.base_update_utils import BaseUpdateUtils, LatestInfoResponse
from version import __version__


RES_ID = "Auto_Resonance"
LATEST_URL = f"https://mirrorchyan.com/api/resources/{RES_ID}/latest"

class MirrorUpdateUtils(BaseUpdateUtils):
    def get_latest_info(self, cdk: str):
        query = {
            "current_version": __version__,
            "cdk": cdk,
            "user_agent": RES_ID
        }
        resposne = requests.get(LATEST_URL, params=query)
        return LatestInfoResponse.model_validate(resposne.json())
