from core.adb import screenshot, input_tap
from core.image import crop_image, show_image
from core.ocr import predict

def get_excption():
    if not_strength():
        return "澄明度不足"

def not_strength():
    image = screenshot()
    image = crop_image(image, (443, 938, 315, 400))
    data = predict(image)
    if not data:
        return False
    if "澄明度不足" in data[0]["text"]:
        input_tap((319, 512))
        return True
    return False
