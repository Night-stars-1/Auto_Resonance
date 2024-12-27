"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-11 20:58:19
LastEditTime: 2024-12-27 23:50:07
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from qfluentwidgets import ConfigItem, QConfig

from app.common.utils import read_json

skill_data: dict = read_json("resources/goods/SkillData.json")

SKILLS = list(skill_data.keys())

# 七号自由港需要在下方特殊适配
CITYS = [
    "七号自由港",
    "澄明数据中心",
    "阿妮塔战备工厂",
    "阿妮塔能源研究所",
    "淘金乐园",
    "曼德矿场",
    "荒原站",
    "铁盟哨站",
    "修格里城",
    "阿妮塔发射中心",
    "海角城",
]
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

    totalMaxBook = ConfigItem("RunningBusiness", "totalMaxBook", 4, None)
    profitThreshold = ConfigItem("RunningBusiness", "profitThreshold", 100000, None)
    priceThreshold = ConfigItem("RunningBusiness", "priceThreshold", 500, None)
    maxGoodsNum = ConfigItem("RunningBusiness", "maxGoodsNum", 625, None)
    tiredProfitThreshold = ConfigItem(
        "RunningBusiness", "tiredProfitThreshold", 12000, None
    )

    for skill in SKILLS:
        locals()[skill] = ConfigItem("SkillLevel", skill, 0, None)

    for city in CITYS:
        # 特殊适配7号自由港
        locals()[city] = ConfigItem("NegotiatePrice", city.replace("七号自由港", "7号自由港"), 0, None)
    buyTired = ConfigItem("NegotiatePrice", "buyTired", 8, None)
    sellTired = ConfigItem("NegotiatePrice", "sellTired", 8, None)

    for station in STATIONS:
        # 特殊适配7号自由港
        locals()[station] = ConfigItem("StationLevel", station.replace("七号自由港", "7号自由港"), 0, None)
