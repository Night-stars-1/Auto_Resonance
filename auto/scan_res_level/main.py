import re
import time

import cv2
from loguru import logger
from qfluentwidgets import qconfig

from app.common.config import cfg
from app.common.signal_bus import signalBus
from app.view.running_business_interface import SKILLS
from core.adb import connect, input_tap, screenshot
from core.image import find_icons_coordinates
from core.ocr import predict
from core.presets import go_home


def sort_coordinates(lv_coordinates):
    # 首先，根据y坐标进行排序
    lv_coordinates.sort(key=lambda x: x[1])

    # 初始化分组列表
    groups = []
    current_group = [lv_coordinates[0]]

    for i in range(1, len(lv_coordinates)):
        # 如果当前坐标的y与前一个y的差距在10以内，视为同一组
        if abs(lv_coordinates[i][1] - lv_coordinates[i-1][1]) <= 10:
            current_group.append(lv_coordinates[i])
        else:
            # 否则，结束当前组的添加，开始新的组
            groups.append(current_group)
            current_group = [lv_coordinates[i]]
    # 添加最后一组
    groups.append(current_group)

    # 对每个组内的元素按照x坐标从小到大进行排序
    for group in groups:
        group.sort(key=lambda x: x[0])

    # 将所有分组合并回一个列表
    sorted_lv_coordinates = [item for group in groups for item in group]
    return sorted_lv_coordinates

def scan_screenshot_characters():
    img = screenshot()
    lv_coordinates = find_icons_coordinates(image=img, icon_path="resources/characters/lv.png")
    lv_coordinates = sort_coordinates(lv_coordinates)

    characters = []
    for lv_coordinate in lv_coordinates:
        data = predict(img_fp=img, cropped_pos1=(lv_coordinate[0]-64, lv_coordinate[1]+16),
                         cropped_pos2=(lv_coordinate[0]+45, lv_coordinate[1]+38))
        characters.append({"name":data[0]["text"], "x":lv_coordinate[0], "y":lv_coordinate[1]})
    return characters

def get_skill_level(character):
    input_tap(pos=(character["x"], character["y"]))
    time.sleep(1)
    input_tap(pos=(1250, 450))
    time.sleep(1)
    img = screenshot()
    text = predict(img_fp=img, cropped_pos1=(944, 434),
                                        cropped_pos2=(1054, 461))[0]["text"]
    level = re.search(r"共振第(\d+)阶段", text).group(1)
    input_tap(pos=(95, 40))
    time.sleep(2)
    return int(level)

def tap_last(characters):
    input_tap(pos=(characters[-1]["x"], characters[-1]["y"]))
    time.sleep(1)
    input_tap(pos=(95, 40))
    time.sleep(2)
    
def get_resonance_level():
    scaned_characters = []
    last_character = ""
    while True:
        tap_last_flag = True
        characters = scan_screenshot_characters()
        for character in characters:
            if character["name"] in SKILLS and character["name"] not in scaned_characters:
                tap_last_flag =False
                scaned_characters.append(character["name"])
                level = get_skill_level(character)
                logger.info(f'{character["name"]}的共振等级:{level}')
                qconfig.set(getattr(cfg, character["name"]), level)
                break

        if tap_last_flag:
            if characters[-1]["name"] == last_character:
                signalBus.skillchanged.emit()
                break
            tap_last(characters)
            last_character = characters[-1]["name"]

def run(
    order: str,
    path: str,
):
    status = connect(order, path)
    if not status:
        logger.error("ADB连接失败")
        return False
    go_home()
    input_tap(pos=(1250, 45))
    time.sleep(2)
    logger.info("开始扫描")
    get_resonance_level()
    logger.info("扫描完成")