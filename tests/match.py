import sys
from pathlib import Path

from loguru import logger

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))


from core.image import match_screenshot
from core.adb import connect, screenshot

connect()
image = screenshot()
logger.info(
    match_screenshot(image, "resources/attack_end.png", [1057, 1255, 593, 669])
)
