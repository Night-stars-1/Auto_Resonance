import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import cv2
import numpy as np

from core.adb import connect, screenshot
from core.image import show_image

connect()


def match_and_draw(img, template, threshold, color):
    h, w = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # 将匹配结果存储在集合中，避免重复
    match_set = set()
    for pt in zip(*loc[::-1]):
        match_set.add((pt[0], pt[1]))

    # 统一标记匹配区域
    for pt in match_set:
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), color, 1)
        score = res[pt[1], pt[0]]
        cv2.putText(
            img,
            f"{score:.2f}",
            (pt[0], pt[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
        )


# 读取原图
# img = cv2.imread("resources/MuMu12-20240404-215502.png")
img = screenshot()
# 模板图片
stastion1 = cv2.imread("tests/image1.png")
stastion2 = cv2.imread("tests/image2.png")
# 阈值
threshold = 0.90

# 对两个模板进行匹配并标记
match_and_draw(img, stastion1, threshold, (0, 255, 0))  # 用绿色标记stastion1的匹配结果
match_and_draw(img, stastion2, threshold, (0, 0, 255))  # 用红色标记stastion2的匹配结果

# 显示结果
cv2.imshow("Detected", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
