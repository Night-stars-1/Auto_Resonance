"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-11 20:58:19
LastEditTime: 2024-12-27 23:51:26
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Dict
from qfluentwidgets import ConfigItem, QConfig

from app.common.utils import read_json

skill_data: dict = read_json("resources/goods/SkillData.json")

SKILLS = list(skill_data.keys())

# 七号自由港需要在下方特殊适配
# CITYS = [
#     "七号自由港",
#     "澄明数据中心",
#     "阿妮塔战备工厂",
#     "阿妮塔能源研究所",
#     "淘金乐园",
#     "曼德矿场",
#     "荒原站",
#     "铁盟哨站",
#     "修格里城",
#     "阿妮塔发射中心",
#     "海角城",
# ]
city_sell_data: Dict[str, Dict[str, int]] = read_json(
    "resources/goods/CityGoodsSellData.json"
)
CITYS = list(city_sell_data.keys())

# 七号自由港需要在下方特殊适配
STATIONS = [
    "七号自由港",
    "澄明数据中心",
    "曼德矿场",
    "修格里城",
    "阿妮塔发射中心",
    "海角城",
]

class RunningBusinessConfig(QConfig):
    """Config of application"""

    BuyCount = ConfigItem("RunBuy", "BuyCount", 0, None)
    
    for city in CITYS:
        # 特殊适配7号自由港
        locals()[f"{city}进货书"] = ConfigItem("CityBook", city.replace("七号自由港", "7号自由港"), 0, None)
        locals()[f"{city}议价次数"] = ConfigItem("CityHaggle", city.replace("七号自由港", "7号自由港"), 0, None)
