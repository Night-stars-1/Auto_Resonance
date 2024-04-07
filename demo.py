"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-04 17:56:16
LastEditTime: 2024-04-05 21:17:17
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from auto.run_business import (
    buy_business,
    click_bargain_button,
    go_business,
    sell_business,
)
from core.adb import connect
from core.presets import click_station, go_home, wait

if __name__ == "__main__":
    connect()
    """
    go_business("buy")
    buy_business([["发动机", "家电", "红茶", "高档餐具"]], 20)
    go_home()
    click_station("铁盟哨站").wait()
    go_business("sell")
    sell_business()
    go_home()
    """
    """
    go_business("buy")
    buy_business([["弹丸加速装置", "精钢", "子弹", "汽油"]], 20)
    go_home()
    click_station("修格里城").wait()
    go_business("sell")
    sell_business()
    go_home()
    """
    click_station("修格里城")
