import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import math

from core.adb import connect, screenshot
from core.image import crop_image, show_image
from core.ocr import predict

connect()
image = screenshot()
# show_image(image)
data = predict(image)
print(data)
