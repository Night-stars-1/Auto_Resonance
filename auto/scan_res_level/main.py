import cv2
from loguru import logger

from core.adb import connect, input_tap, screenshot
from core.image import crop_image, find_icons_coordinates, get_mse, get_ssim, show_image
from core.ocr import predict


def get_resonance_level():
    img = screenshot()
    lv_coordinates = find_icons_coordinates(image=img, icon_path="resources/characters/lv.png")
    i=0
    for lv_coordinate in lv_coordinates:
        data = predict(img_fp=img, cropped_pos1=(lv_coordinate[0]-24, lv_coordinate[1]+16),
                         cropped_pos2=(lv_coordinate[0]+45, lv_coordinate[1]+38))
        logger.info([item["text"] for item in data])
        croped_image = crop_image(screenshot=img.copy(), 
                             cropped_pos1=(lv_coordinate[0]+14, lv_coordinate[1]-200),
                             cropped_pos2=(lv_coordinate[0]+46, lv_coordinate[1]-160))
        
        max_ssim = -1
        max_ssim_lv = -1
        for lv in range(6):
            lv_img = cv2.imread(f"resources/characters/lv{lv}.png")
            # mse = get_mse(imageA=croped_image, imageB=lv_img)
            # logger.info(f"lv:{lv},mse:{mse}")
            # if mse < min_mse:
            #     min_mse = mse
            #     min_mse_lv = lv

            ssim = get_ssim(imageA=croped_image, imageB=lv_img)
            logger.info(f"lv:{lv},ssim:{ssim}")
            if ssim > max_ssim:
                max_ssim = ssim
                max_ssim_lv = lv


        logger.info(f"识别的共振等级:{max_ssim_lv}")
        

def run(
    order: str,
    path: str,
):
    status = connect(order, path)
    if not status:
        logger.error("ADB连接失败")
        return False
    logger.info("开始扫描")
    get_resonance_level()
    logger.info("扫描完成")