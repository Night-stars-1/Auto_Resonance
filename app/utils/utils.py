
import re


def is_chinese(text: str):
    """
    检查整个字符串是否包含中文

    :param text: 需要检查的字符串
    :return: bool
    """
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(chinese_pattern.search(text))
