
from pathlib import Path
import sys

ROOT_PATH = Path().resolve()
"""项目根目录"""
if getattr(sys, 'frozen', False):
    ROOT_PATH = Path(sys.executable).parent.resolve()

RESOURCE_PATH = ROOT_PATH / "resources"
"""资源路径"""
APP_PATH = RESOURCE_PATH / "app"
"""应用资源路径"""
QSS_PATH = APP_PATH / "qss"
"""QSS样式表路径"""
ICON_PATH = APP_PATH / "icons"
"""图标资源路径"""
GOODS_PATH = RESOURCE_PATH / "goods"
"""商品资源路径"""