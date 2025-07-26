import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from core.control.control import connect
from core.preset.station import STATION

if __name__ == "__main__":
    connect()
    STATION(True).join_wait_fight()
