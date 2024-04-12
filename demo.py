"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:56:16
LastEditTime: 2024-04-13 01:12:47
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from loguru import logger

from auto.run_business import run


if __name__ == "__main__":
    run(
        {
            "7号自由港": 3,
            "修格里城": 3,
            "曼德矿场": 3,
            "淘金乐园": 3,
            "澄明数据中心": 3,
            "荒原站": 3,
            "铁盟哨站": 3,
            "阿妮塔战备工厂": 3,
            "阿妮塔能源研究所": 3,
            "priceThreshold": 500,
        }
    )
    # click_station("修格里城")
