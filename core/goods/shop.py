# TODO: 1.数据模型化 2.提高可读性

import itertools
import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List

from loguru import logger

from core.models import app
from core.models.city_goods import (
    CityDataModel,
    RouteModel,
    RoutesModel,
)
from ..models.goods import GoodInfoModel, GoodModel, GoodsModel


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
    if book_profit == 100:
        return "未配置进货书，单书利润为0"
    message = f"""{route[0].buy_city_name}<->{route[0].sell_city_name}:
{route[0].buy_city_name}:
    商品数量: {to_goods_num}
    商品顺序: {"->".join(route[0].goods_data.keys())}
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
    商品顺序: {"->".join(route[1].goods_data.keys())}
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

with open("resources/goods/SkillData.json", "r", encoding="utf-8") as file:
    skill_data: dict = json.load(file)

class SHOP:
    def __init__(self, goods_data: GoodsModel) -> None:
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
        self.city_book = app.RunningBusiness
        """城市最大单次进货书"""
        self.goods_addition: Dict[str, int] = self.get_goods_addition()
        """商品附加"""
        self.all_city_info: Dict[str, CityDataModel] = (
            self.get_city_data_by_city_level()
        )
        """城市税率等声望信息"""
        self.negotiate_price = app.NegotiatePrice
        """议价次数和单次疲劳"""
        self.max_goods_num = app.RunningBusiness.maxGoodsNum
        """最大商品数量"""
        self.last_route_profit = 0
        """路线利润缓存数据"""

    def get_goods_addition(self) -> Dict[str, int]:
        goods_addition: dict = {}
        """商品附加"""
        for role_name, role_level in app.SkillLevel.items():
            role_skill_data = skill_data.get(role_name, [])

            for skill_affect in role_skill_data:
                if int(role_level) >= int(skill_affect):
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

    def get_city_data_by_city_level(self) -> Dict[str, CityDataModel]:
        station_level = app.StationLevel
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
            :param price: 商品价格, 砍价前
            :param num: 商品数量
            :param city_name: 城市名称
            :param good_name: 商品名称
        """
        buy_num = self.all_city_info.get(
            city_name, CityDataModel()
        ).buy_num  # 城市声望数量加成
        skill_num = self.goods_addition.get(good_name, 0)  # 角色技能增加的数量
        new_num = round5(num * (1 + buy_num + skill_num))
        # tax_rate = self.all_city_info[city_name].revenue  # 税率
        new_price = round5(price * 0.8)  # 砍抬一律0.2  # 砍价后的价格
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
        revenue = round5(no_tax_profit * tax_rate)  # 税收

        new_sell_price = no_revenue_sell_price - revenue

        # if city_name == "阿妮塔战备工厂" and good_name != "1阿妮塔小型桦树发电机":
        #     print(
        #         f"{city_name=} {good_name=} {new_sell_price=} {buy_price=} {no_revenue_sell_price=} {no_tax_profit=} {revenue}"
        #     )

        return new_sell_price, no_tax_profit

    def get_goods_profit(
        self, goods: Dict[str, GoodModel], buy_city_name: str, sell_city_name: str
    ):
        """
        说明:
            获取所有商品利润
        """
        good_info: List[GoodInfoModel] = []
        for good_name, good in goods.items():
            if good_name not in self.sell_goods[sell_city_name]:
                # logger.error(f"{sell_city_name}没有{name}的数据")
                continue
            buy_price, buy_num = self.get_good_buy_price(
                good.price, good.num, buy_city_name, good_name
            )
            sell_price, profit = self.get_good_sell_price(
                buy_price, sell_city_name, good_name
            )
            good_info.append(
                GoodInfoModel(
                    name=good_name,
                    buy_price=buy_price,
                    sell_price=sell_price,
                    profit=profit,
                    buy_num=buy_num,
                )
            )
        sorted_good_info = sorted(good_info, key=lambda item: item.profit, reverse=True)
        return sorted_good_info

    def get_need_buy_use_first(
        self, buy_city_name: str, sell_city_name: str, book: int = 0
    ):
        """
        说明:
            获取需要购买的物品的信息（先使用进货书）
        参数:
            :param buy_city_name: 购买城市名称
            :param sell_city_name: 出售城市名称
            :param book: 最大进货书数量
        """
        goods = self.buy_goods[buy_city_name]  # 购买城市的商品信息
        """
        sorted_goods = sorted(
            goods.items(), key=lambda item: item[1].isSpeciality, reverse=True
        )  # 按照是否特产排序
        speciality_num = len([good for good in goods.values() if good.isSpeciality])
        """
        buy_argaining_num = self.negotiate_price.get_tired(buy_city_name, -1) # 购买议价次数
        sell_argaining_num = self.negotiate_price.get_tired(sell_city_name, -1) # 出售议价次数
        # 总疲劳
        city_tired = (
            city_tired_data.get(f"{buy_city_name}-{sell_city_name}", 99999)
            + buy_argaining_num * self.negotiate_price.buyTired  # 购买总疲劳
            + sell_argaining_num * self.negotiate_price.sellTired  # 出售总疲劳
        )
        # 目标站点的商品价格信息
        route_data: RouteModel = RouteModel(
            buy_city_name=buy_city_name,
            sell_city_name=sell_city_name,
            city_tired=city_tired,
            buy_argaining_num=buy_argaining_num,
            sell_argaining_num=sell_argaining_num,
            book=book,
        )
        if buy_argaining_num == -1 or sell_argaining_num == -1:
            return None # 当议价次数为-1时候，过滤该路线方案
        sorted_good_info = self.get_goods_profit(goods, buy_city_name, sell_city_name)
        for good_info in sorted_good_info:
            num = min(
                good_info.buy_num * (book + 1),
                self.max_goods_num - route_data.num,
            )  # 确保购买数量不超过最大商品数量
            # good_profit = good_info.profit * num  # 商品利润
            route_data.goods_data.setdefault(good_info.name, RouteModel.GoodsData())
            route_data.goods_data[good_info.name].num += num
            route_data.goods_data[good_info.name].buy_price += good_info.buy_price
            route_data.goods_data[good_info.name].sell_price += good_info.sell_price
            route_data.goods_data[good_info.name].profit += good_info.profit
            route_data.num += num
            route_data.profit += good_info.profit * num
            route_data.buy_price += good_info.buy_price * num
            route_data.sell_price += good_info.sell_price * num

        # 计算所有商品附税购买价
        tax_rate = self.all_city_info[buy_city_name].revenue  # 税率
        route_data.buy_price = round5((1+tax_rate) * route_data.buy_price)

        route_data.tired_profit = round5(route_data.profit / city_tired)
        # 通过缓存利润计算单书利润
        last_profit = 0 if book == 0 else self.last_route_profit
        # 缓存路线方案利润
        self.last_route_profit = route_data.profit

        route_data.book_profit = route_data.profit - last_profit
        if route_data.book_profit < self.city_book.profitThreshold and book != 0:
            # 当单书利润小于阈值时，过滤该路线
            return None
        return route_data

    def get_route_profit(self):
        """
        说明:
            获取路线利润
        返回:
            :return: 路线数据
        """
        total_max_book = self.city_book.totalMaxBook
        routes: List[RoutesModel] = []
        for city1, city2 in itertools.combinations(set(self.buy_goods.keys()), 2):
            for max_book in range(total_max_book + 1):
                if city1 not in self.all_city_info or city2 not in self.all_city_info:
                    continue
                city_routes = RoutesModel()
                target1 = max(
                    (
                        route
                        for book in range(max_book + 1)
                        if (route := self.get_need_buy_use_first(city1, city2, book))
                    ),
                    key=lambda route: route.tired_profit,
                    default=None
                )
                target2 = max(
                    (
                        route
                        for book in range(total_max_book - max_book + 1)
                        if (route := self.get_need_buy_use_first(city2, city1, book))
                    ),
                    key=lambda route: route.tired_profit,
                    default=None
                )
                if target1 is None or target2 is None:
                    continue # 该路线无有效线路，过滤
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
        """
        benchmark_profit = sum(route.book_profit for route in routes) / len(routes)

        optimal_route = max(
            (route for route in routes if route.book_profit > benchmark_profit),
            key=lambda route: route.tired_profit,
            default=RoutesModel(),  # 如果没有符合条件的对象，返回None
        )
        for good in routes:
            logger.info(show(good))
        """
        optimal_route = max(
            routes,
            key=lambda route: route.tired_profit,
            default=RoutesModel(),  # 如果没有符合条件的对象，返回None
        )
        """
        # 根据利润排序低价值商品
        optimal_route.city_data[0].normal_goods = {
            k: v
            for k, v in sorted(
                optimal_route.city_data[0].normal_goods.items(),
                key=lambda item: item[1],
            )
        }
        if len(optimal_route.city_data[0].buy_goods) == 0:
            nomal_good = optimal_route.city_data[0].normal_goods.popitem()
            optimal_route.city_data[0].buy_goods = {nomal_good[0]: nomal_good[1]}
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
        if len(optimal_route.city_data[1].buy_goods) == 0:
            nomal_good = optimal_route.city_data[1].normal_goods.popitem()
            optimal_route.city_data[1].buy_goods = {nomal_good[0]: nomal_good[1]}
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
        """
        return optimal_route
