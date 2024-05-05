"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-11 20:58:19
LastEditTime: 2024-04-27 21:49:52
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from qfluentwidgets import ConfigItem, QConfig


class RunningBusinessConfig(QConfig):
    """Config of application"""

    totalMaxBook = ConfigItem("RunningBusiness", "totalMaxBook", 4, None)
    profitThreshold = ConfigItem("RunningBusiness", "profitThreshold", 100000, None)
    priceThreshold = ConfigItem("RunningBusiness", "priceThreshold", 500, None)
    maxGoodsNum = ConfigItem("RunningBusiness", "maxGoodsNum", 625, None)
    tiredProfitThreshold = ConfigItem("RunningBusiness", "tiredProfitThreshold", 12000, None)

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

    七号自由港砍抬次数 = ConfigItem("NegotiatePrice", "7号自由港", 0, None)
    澄明数据中心砍抬次数 = ConfigItem("NegotiatePrice", "澄明数据中心", 0, None)
    阿妮塔战备工厂砍抬次数 = ConfigItem("NegotiatePrice", "阿妮塔战备工厂", 0, None)
    阿妮塔能源研究所砍抬次数 = ConfigItem("NegotiatePrice", "阿妮塔能源研究所", 0, None)
    淘金乐园砍抬次数 = ConfigItem("NegotiatePrice", "淘金乐园", 0, None)
    曼德矿场砍抬次数 = ConfigItem("NegotiatePrice", "曼德矿场", 0, None)
    荒原站砍抬次数 = ConfigItem("NegotiatePrice", "荒原站", 0, None)
    铁盟哨站砍抬次数 = ConfigItem("NegotiatePrice", "铁盟哨站", 0, None)
    修格里城砍抬次数 = ConfigItem("NegotiatePrice", "修格里城", 0, None)
    阿妮塔发射中心砍抬次数 = ConfigItem("NegotiatePrice", "阿妮塔发射中心", 0, None)
    buyTired = ConfigItem("NegotiatePrice", "buyTired", 8, None)
    sellTired = ConfigItem("NegotiatePrice", "sellTired", 8, None)

    七号自由港声望 = ConfigItem("StationLevel", "7号自由港", 0, None)
    澄明数据中心声望 = ConfigItem("StationLevel", "澄明数据中心", 0, None)
    曼德矿场声望 = ConfigItem("StationLevel", "曼德矿场", 0, None)
    修格里城声望 = ConfigItem("StationLevel", "修格里城", 0, None)
    阿妮塔发射中心声望 = ConfigItem("StationLevel", "阿妮塔发射中心", 0, None)
