"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-11 20:58:19
LastEditTime: 2024-04-14 02:37:43
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from qfluentwidgets import ConfigItem, QConfig

SKILLS = [
    "朱利安",
    "狮鬃",
    "魇",
    "塞西尔",
    "雷火",
    "黛丝莉",
    "艾略特",
    "静流",
    "多萝西",
    "卡莲",
    "星花",
    "瑞秋",
    "菲妮娅",
    "瓦伦汀",
    "阿知波",
    "闻笙",
    "山岚",
    "叶珏",
    "隼",
    "奈弥",
    "伊尔",
    "甘雅",
    "妮蔻拉",
    "卡洛琳",
    "海因里希",
]


class RunningBusinessConfig(QConfig):
    """Config of application"""

    七号自由港进货书 = ConfigItem("RunningBusiness", "7号自由港", 0, None)
    澄明数据中心进货书 = ConfigItem("RunningBusiness", "澄明数据中心", 0, None)
    阿妮塔战备工厂进货书 = ConfigItem("RunningBusiness", "阿妮塔战备工厂", 0, None)
    阿妮塔能源研究所进货书 = ConfigItem("RunningBusiness", "阿妮塔能源研究所", 0, None)
    淘金乐园进货书 = ConfigItem("RunningBusiness", "淘金乐园", 0, None)
    曼德矿场进货书 = ConfigItem("RunningBusiness", "曼德矿场", 0, None)
    荒原站进货书 = ConfigItem("RunningBusiness", "荒原站", 0, None)
    铁盟哨站进货书 = ConfigItem("RunningBusiness", "铁盟哨站", 0, None)
    修格里城进货书 = ConfigItem("RunningBusiness", "修格里城", 0, None)
    priceThreshold = ConfigItem("RunningBusiness", "priceThreshold", 500, None)
    maxGoodsNum = ConfigItem("RunningBusiness", "maxGoodsNum", 625, None)

    朱利安 = ConfigItem("SkillLevel", "朱利安", 0, None)
    狮鬃 = ConfigItem("SkillLevel", "狮鬃", 0, None)
    魇 = ConfigItem("SkillLevel", "魇", 0, None)
    塞西尔 = ConfigItem("SkillLevel", "塞西尔", 0, None)
    雷火 = ConfigItem("SkillLevel", "雷火", 0, None)
    黛丝莉 = ConfigItem("SkillLevel", "黛丝莉", 0, None)
    艾略特 = ConfigItem("SkillLevel", "艾略特", 0, None)
    静流 = ConfigItem("SkillLevel", "静流", 0, None)
    多萝西 = ConfigItem("SkillLevel", "多萝西", 0, None)
    卡莲 = ConfigItem("SkillLevel", "卡莲", 0, None)
    星花 = ConfigItem("SkillLevel", "星花", 0, None)
    瑞秋 = ConfigItem("SkillLevel", "瑞秋", 0, None)
    菲妮娅 = ConfigItem("SkillLevel", "菲妮娅", 0, None)
    瓦伦汀 = ConfigItem("SkillLevel", "瓦伦汀", 0, None)
    阿知波 = ConfigItem("SkillLevel", "阿知波", 0, None)
    闻笙 = ConfigItem("SkillLevel", "闻笙", 0, None)
    山岚 = ConfigItem("SkillLevel", "山岚", 0, None)
    叶珏 = ConfigItem("SkillLevel", "叶珏", 0, None)
    隼 = ConfigItem("SkillLevel", "隼", 0, None)
    奈弥 = ConfigItem("SkillLevel", "奈弥", 0, None)
    伊尔 = ConfigItem("SkillLevel", "伊尔", 0, None)
    甘雅 = ConfigItem("SkillLevel", "甘雅", 0, None)
    妮蔻拉 = ConfigItem("SkillLevel", "妮蔻拉", 0, None)
    卡洛琳 = ConfigItem("SkillLevel", "卡洛琳", 0, None)
    海因里希 = ConfigItem("SkillLevel", "海因里希", 0, None)

    七号自由港砍抬疲劳 = ConfigItem("CityTired", "7号自由港", 30, None)
    澄明数据中心砍抬疲劳 = ConfigItem("CityTired", "澄明数据中心", 30, None)
    阿妮塔战备工厂砍抬疲劳 = ConfigItem("CityTired", "阿妮塔战备工厂", 30, None)
    阿妮塔能源研究所砍抬疲劳 = ConfigItem("CityTired", "阿妮塔能源研究所", 30, None)
    淘金乐园砍抬疲劳 = ConfigItem("CityTired", "淘金乐园", 30, None)
    曼德矿场砍抬疲劳 = ConfigItem("CityTired", "曼德矿场", 30, None)
    荒原站砍抬疲劳 = ConfigItem("CityTired", "荒原站", 30, None)
    铁盟哨站砍抬疲劳 = ConfigItem("CityTired", "铁盟哨站", 30, None)
    修格里城砍抬疲劳 = ConfigItem("CityTired", "修格里城", 30, None)

    七号自由港声望 = ConfigItem("StationLevel", "7号自由港", 1, None)
    澄明数据中心声望 = ConfigItem("StationLevel", "澄明数据中心", 1, None)
    曼德矿场声望 = ConfigItem("StationLevel", "曼德矿场", 1, None)
    修格里城声望 = ConfigItem("StationLevel", "修格里城", 1, None)
