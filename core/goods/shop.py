# TODO: 1.数据模型化 2.提高可读性

import itertools
import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List

from loguru import logger

from core.models.city_goods import (
    CityDataModel,
    RouteModel,
    RoutesModel,
)
from ..models.goods import GoodsModel


def round5(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def show(routes: RoutesModel):
    route = routes.city_data
    to_goods_num = ",".join(
        [f"{name}{route[0].goods_data[name].num}" for name in route[0].goods_data]
    )
    back_goods_num = ",".join(
        [f"{name}{route[1].goods_data[name].num}" for name in route[1].goods_data]
    )
    profit = route[0].profit + route[1].profit
    book = route[0].book + route[1].book
    city_tired = route[0].city_tired + route[1].city_tired
    tired_profit = round5(profit / city_tired)
    book_profit = book and round5(profit / book)
    if book_profit == 0:
        return "未配置进货书，单书利润为0"
    message = f"""{route[0].buy_city_name}<->{route[0].sell_city_name}:
{route[0].buy_city_name}:
    商品数量: {to_goods_num}
    商品顺序: {"->".join(route[0].primary_goods)+"->".join(route[0].secondary_goods)}
    商品总量: {route[0].num}
    购买价格: {route[0].buy_price}
    出售价格: {route[0].sell_price}
    商品利润: {route[0].profit}
    所需疲劳: {route[0].city_tired}
    疲劳利润: {route[0].tired_profit}
    单书利润: {route[0].book_profit}
    书本数量: {route[0].book}
{route[0].sell_city_name}:
    商品数量: {back_goods_num}
    商品顺序: {"->".join(route[1].primary_goods)+"->".join(route[1].secondary_goods)}
    商品总量: {route[1].num}
    购买价格: {route[1].buy_price}
    出售价格: {route[1].sell_price}
    商品利润: {route[1].profit}
    所需疲劳: {route[1].city_tired}
    疲劳利润: {route[1].tired_profit}
    单书利润: {route[1].book_profit}
    书本数量: {route[1].book}
总计:
    利润: {profit}
    所需疲劳: {city_tired}
    疲劳利润: {tired_profit}
    单书利润: {book_profit}
    书本数量: {book}"""

    return message


with open("resources/goods/CityGoodsData.json", "r", encoding="utf-8") as file:
    city_goods_data = json.load(file)

with open("resources/goods/CityData.json", "r", encoding="utf-8") as file:
    city_data = json.load(file)

with open("resources/goods/AttachedToCityData.json", "r", encoding="utf-8") as file:
    attached_to_city_data: Dict[str, str] = json.load(file)

with open("resources/goods/CityTiredData.json", "r", encoding="utf-8") as file:
    city_tired_data: dict = json.load(file)

skill_data = {
    "朱利安": {
        1: {"goods": ["斑节虾"], "param": 0.2},
        4: {"goods": ["斑节虾", "人工晶花", "桦石发财树", "石墨烯"], "param": 0.2},
    },
    "狮鬃": {
        1: {"goods": ["荧光棒"], "param": 0.2},
        4: {"goods": ["扬声器"], "param": 0.2},
    },
    "魇": {1: {"goods": ["刀具"], "param": 0.2}, 5: {"goods": ["刀具"], "param": 0.1}},
    "塞西尔": {
        4: {"goods": ["香水"], "param": 0.2},
        5: {"goods": ["香水"], "param": 0.3},
    },
    "雷火": {4: {"goods": ["曼德工具箱"], "param": 0.2}},
    "黛丝莉": {
        4: {"goods": ["毛绒玩具"], "param": 0.2},
        5: {"goods": ["毛绒玩具"], "param": 0.1},
    },
    "艾略特": {4: {"goods": ["游戏卡带", "游戏机"], "param": 0.2}},
    "静流": {4: {"goods": ["珍珠", "学会书籍", "单晶硅", "大龙虾"], "param": 0.2}},
    "多萝西": {
        4: {"goods": ["弹丸加速装置"], "param": 0.2},
        5: {"goods": ["弹丸加速装置"], "param": 0.1},
    },
    "卡莲": {4: {"goods": ["高端护肤品", "香水", "火腿", "鱼子酱"], "param": 0.2}},
    "星花": {1: {"goods": ["人工晶花"], "param": 0.2}},
    "瑞秋": {4: {"goods": ["医药品"], "param": 0.2}},
    "菲妮娅": {
        4: {"goods": ["大龙虾"], "param": 0.2},
        5: {"goods": ["大龙虾"], "param": 0.1},
    },
    "瓦伦汀": {
        4: {"goods": ["学会书籍"], "param": 0.2},
        5: {"goods": ["学会书籍"], "param": 0.1},
    },
    "阿知波": {
        4: {"goods": ["拼装模型"], "param": 0.2},
        5: {"goods": ["拼装模型"], "param": 0.1},
    },
    "闻笙": {
        4: {"goods": ["限定公仔"], "param": 0.2},
        5: {"goods": ["限定公仔"], "param": 0.1},
    },
    "山岚": {4: {"goods": ["折扇"], "param": 0.2}},
    "叶珏": {
        1: {"goods": ["红茶"], "param": 0.2},
        4: {"goods": ["家用太阳能电池组"], "param": 0.2},
        5: {"goods": ["红茶"], "param": 0.1},
    },
    "隼": {1: {"goods": ["发动机"], "param": 0.2}},
    "奈弥": {
        1: {"goods": ["金箔酒"], "param": 0.2},
        5: {"goods": ["金箔酒"], "param": 0.1},
    },
    "伊尔": {
        1: {"goods": ["阿妮塔101民用无人机"], "param": 0.2},
        5: {"goods": ["阿妮塔101民用无人机"], "param": 0.1},
    },
    "甘雅": {
        4: {"goods": ["图形加速卡", "曼德工具箱"], "param": 0.2},
        5: {"goods": ["图形加速卡", "曼德工具箱"], "param": 0.1},
    },
    "妮蔻拉": {
        4: {
            "goods": [
                "阿妮塔小型桦树发电机",
                "石墨烯电池",
                "家用太阳能电池组",
                "阿妮塔101民用无人机",
            ],
            "param": 0.2,
        },
        5: {
            "goods": [
                "阿妮塔小型桦树发电机",
                "石墨烯电池",
                "家用太阳能电池组",
                "阿妮塔101民用无 人机",
            ],
            "param": 0.1,
        },
    },
    "卡洛琳": {
        4: {"goods": ["石墨烯"], "param": 0.2},
        5: {"goods": ["石墨烯"], "param": 0.1},
    },
    "海因里希": {
        4: {"goods": ["拼装模型"], "param": 0.2},
        5: {"goods": ["拼装模型"], "param": 0.1},
    },
}


class SHOP:
    def __init__(
        self,
        goods_data: GoodsModel,
        city_book: Dict[str, int],
        skill_level: Dict[str, int],
        station_level: Dict[str, int],
        negotiate_price: Dict[str, int],
        max_goods_num: int,
    ) -> None:
        """
        说明:
            跑商基类
        参数:
            :param goods_data: 商品数据
            :param city_book: 城市进货书信息
            :param skill_level: 角色共振等级
            :param station_level: 站点声望等级等级
            :param negotiate_price: 议价次数和单次疲劳
            :param max_goods_num: 最大商品数量
        """
        self.goods_data = goods_data
        self.buy_goods = self.goods_data.buy_goods
        """城市可购买的商品信息"""
        self.sell_goods = self.goods_data.sell_goods
        """城市可出售的商品信息"""
        self.city_book = city_book
        """城市最大单次进货书"""
        self.goods_addition: Dict[str, int] = self.get_goods_addition(skill_level)
        """商品附加"""
        self.all_city_info: Dict[str, CityDataModel] = self.get_city_data_by_city_level(
            station_level
        )
        """城市税率等声望信息"""
        self.negotiate_price = negotiate_price
        """议价次数和单次疲劳"""
        self.max_goods_num = max_goods_num
        """最大商品数量"""

    def get_goods_addition(self, skill_level: Dict[str, int]) -> Dict[str, int]:
        goods_addition: dict = {}
        """商品附加"""
        for role_name, role_level in skill_level.items():
            role_skill_data = skill_data.get(role_name, [])

            for skill_affect in role_skill_data:
                if role_level >= int(skill_affect):
                    goods, param = (
                        role_skill_data[skill_affect]["goods"],
                        role_skill_data[skill_affect]["param"],
                    )

                    for good_name in goods:
                        if good_name not in goods_addition:
                            goods_addition[good_name] = param
                        else:
                            goods_addition[good_name] += param
        return goods_addition

    def get_city_data_by_city_level(
        self,
        station_level: Dict[str, int],
    ) -> Dict[str, CityDataModel]:
        city_level_data = {}
        for attached_name, station_name in attached_to_city_data.items():
            if station_name not in station_level.keys():
                continue
            level = station_level[station_name]
            city_level_data[attached_name] = CityDataModel.model_validate(
                city_data[station_name][level]
            )
        return city_level_data

    def get_good_buy_price(self, price, num, city_name, good_name):
        """
        说明:
            获取购买商品的价格
        参数:
            :param price: 商品价格
            :param num: 商品数量
            :param city_name: 城市名称
            :param good_name: 商品名称
        """
        buy_num = self.all_city_info.get(
            city_name, CityDataModel()
        ).buy_num  # 城市声望数量加成
        skill_num = self.goods_addition.get(good_name, 0)  # 角色技能增加的数量
        new_num = round5(num * (1 + buy_num + skill_num))
        tax_rate = self.all_city_info[city_name].revenue  # 税率
        new_price = round5(
            price * (1 - 0.2 + tax_rate)  # 砍价前的价格  # 砍抬一律0.2
        )  # 砍价后的价格
        return new_price, new_num

    def get_good_sell_price(self, buy_price: int, city_name: str, good_name: str):
        """
        说明:
            获取出售商品的价格
        参数:
            :param buy_price: 购买价格
            :param city_name: 城市名称
            :param good_name: 商品名称
        """
        base_sell_price = self.sell_goods[city_name][
            good_name
        ].price  # 不带税的售价，砍抬前
        no_revenue_sell_price = round5(
            base_sell_price * (1 + 0.2)
        )  # 不带税的售价, 抬价后
        tax_rate = self.all_city_info[city_name].revenue  # 税率
        no_tax_profit = no_revenue_sell_price - buy_price  # 不带税的利润, 单个商品
        revenue = (no_revenue_sell_price - buy_price) * tax_rate  # 税收

        new_sell_price = round5((no_revenue_sell_price - revenue))
        return new_sell_price, no_tax_profit

    def get_pending_purchase(self, buy_city_name: str, sell_city_name: str, max_book: int = 0):
        """
        说明:
            获取需要购买的物品的信息
        参数:
            :param buy_city_name: 购买城市名称
            :param sell_city_name: 出售城市名称
            :param max_book: 最大书本数量
        """
        goods = self.buy_goods[buy_city_name] # 购买城市的商品信息
        sorted_goods = sorted(
            goods.items(), key=lambda item: item[1].isSpeciality, reverse=True
        ) # 按照是否特产排序
        buy_argaining_num = self.negotiate_price.get(buy_city_name, 0) # 购买议价次数
        sell_argaining_num = self.negotiate_price.get(sell_city_name, 0) # 出售议价次数
        # 总疲劳
        city_tired = (
            city_tired_data.get(f"{buy_city_name}-{sell_city_name}", 99999)
            + buy_argaining_num * self.negotiate_price.get("buyTired", 0) # 购买总疲劳
            + sell_argaining_num * self.negotiate_price.get("sellTired", 0) # 出售总疲劳
        )
        # 目标站点的商品价格信息
        route_price_data: RouteModel = RouteModel(
            buy_city_name=buy_city_name,
            sell_city_name=sell_city_name,
            city_tired=city_tired,
            buy_argaining_num=buy_argaining_num,
            sell_argaining_num=sell_argaining_num,
        )
        while route_price_data.num < self.max_goods_num and route_price_data.book < max_book:  # 直到货仓被装满
            old_route_price_data = route_price_data.model_copy()
            route_price_data.book += 1
            for good_name, good in sorted_goods:
                if good_name not in self.sell_goods[sell_city_name]:
                    # logger.error(f"{sell_city_name}没有{name}的数据")
                    continue
                buy_price, buy_num = self.get_good_buy_price(
                    good.price, good.num, buy_city_name, good_name
                )
                num = min(
                    buy_num,
                    self.max_goods_num - route_price_data.num,
                )  # 确保购买数量不超过最大商品数量
                # print(f"{buy_city_name}:{name}=>{buy_price} {buy_num}")
                sell_price, profit = self.get_good_sell_price(
                    buy_price, sell_city_name, good_name
                )
                good_profit = profit * num # 商品利润
                # print(f"{buy_city_name}<=>{sell_city_name}:{good_name}=>{sell_price} {profit * num}")
                if profit >= self.city_book["priceThreshold"] or good.isSpeciality:
                    if profit >= 1000:
                        route_price_data.buy_goods[good_name] = profit
                    else:
                        route_price_data.normal_goods[good_name] = profit
                    route_price_data.goods_data.setdefault(good_name, RouteModel.GoodsData())
                    route_price_data.goods_data[good_name].num += num
                    route_price_data.goods_data[good_name].buy_price += buy_price
                    route_price_data.goods_data[good_name].sell_price += sell_price
                    route_price_data.goods_data[good_name].profit += good_profit
                    route_price_data.num += num
                    route_price_data.profit += good_profit
                    route_price_data.buy_price += buy_price * num
                    route_price_data.sell_price += sell_price * num
                else:
                    route_price_data.normal_goods[good_name] = profit

            if route_price_data.book and route_price_data.profit / route_price_data.book < self.city_book["profitThreshold"]: # 判断是否小于进货书利润阈值
                route_price_data = old_route_price_data # 小于进货书利润阈值，本次计算无效，结束计算
                break

        route_price_data.tired_profit = round5(route_price_data.profit / city_tired)
        route_price_data.book_profit = route_price_data.book and round5(route_price_data.profit / route_price_data.book)
        return route_price_data

    def get_route_profit(self):
        """
        说明:
            获取路线利润
        返回:
            :return: 路线数据
        """
        total_max_book = self.city_book["totalMaxBook"]
        routes: List[RoutesModel] = []
        for city1, city2 in itertools.combinations(set(self.buy_goods.keys()), 2):
            for max_book in range(1, total_max_book+1):
                if city1 not in self.all_city_info or city2 not in self.all_city_info:
                    continue
                city_routes = RoutesModel()
                target1 = self.get_pending_purchase(city1, city2, max_book)
                target2 = self.get_pending_purchase(city2, city1, total_max_book-max_book)
                city_routes.city_data = [target1, target2]
                # 总计
                city_routes.book = (
                    city_routes.city_data[0].book + city_routes.city_data[1].book
                )
                city_routes.city_tired = (
                    city_routes.city_data[0].city_tired
                    + city_routes.city_data[1].city_tired
                )
                city_routes.profit = (
                    city_routes.city_data[0].profit + city_routes.city_data[1].profit
                )
                city_routes.tired_profit = round5(
                    city_routes.profit / city_routes.city_tired
                )
                city_routes.book_profit = city_routes.book and round5(
                    city_routes.profit / city_routes.book
                )
                routes.append(city_routes)
        return routes

    def get_optimal_route(self):
        """
        说明:
            获取往返路线的最优路线
        """
        # TODO 也许需要改成异步
        routes = self.get_route_profit()
        benchmark_profit = sum(route.book_profit for route in routes) / len(routes)

        optimal_route = max(
            (route for route in routes if route.book_profit > benchmark_profit),
            key=lambda route: route.tired_profit,
            default=RoutesModel(),  # 如果没有符合条件的对象，返回None
        )
        """
        for good in routes:
            logger.info(show(good))
        """
        # 根据利润排序低价值商品
        optimal_route.city_data[0].normal_goods = {
            k: v
            for k, v in sorted(
                optimal_route.city_data[0].normal_goods.items(),
                key=lambda item: item[1],
            )
        }
        # 根据利润重新排序商品，避免高价值商品因为满载而无法购买
        optimal_route.city_data[0].primary_goods = [
            good[0]
            for good in sorted(
                optimal_route.city_data[0].buy_goods.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]
        optimal_route.city_data[0].secondary_goods = [
            good[0]
            for good in sorted(
                optimal_route.city_data[0].normal_goods.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]

        # 根据利润排序低价值商品
        optimal_route.city_data[1].normal_goods = {
            k: v
            for k, v in sorted(
                optimal_route.city_data[1].normal_goods.items(),
                key=lambda item: item[1],
            )
        }
        # 根据利润重新排序商品，避免高价值商品因为满载而无法购买
        optimal_route.city_data[1].primary_goods = [
            good[0]
            for good in sorted(
                optimal_route.city_data[1].buy_goods.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]
        optimal_route.city_data[1].secondary_goods = [
            good[0]
            for good in sorted(
                optimal_route.city_data[1].normal_goods.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]
        return optimal_route
