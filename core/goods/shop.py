# TODO: 1.数据模型化 2.提高可读性

import json
from decimal import Decimal, ROUND_HALF_UP
from itertools import combinations
from typing import Dict, List, Literal, Tuple

from core.models.city_goods import RouteModel, RoutesModel, TargetGoodModel
from ..models.goods import GoodModel, GoodsModel
from ..models.srap import SrapRequestModel
from ..models.config import RunningBusinessModel, config as config_model


def round5(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


with open("resources/goods/CityGoodsData.json", "r", encoding="utf-8") as file:
    city_goods_data = json.load(file)

with open("resources/goods/CityData.json", "r", encoding="utf-8") as file:
    city_data = json.load(file)

with open("resources/goods/AttachedToCityData.json", "r", encoding="utf-8") as file:
    attached_to_city_data: dict = json.load(file)

with open("resources/goods/CityTiredData.json", "r", encoding="utf-8") as file:
    city_tired_data: dict = json.load(file)

skill_data = {
    "朱利安": {1: {"goods": ["斑节虾"], "param": 0.2}},
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
    "多萝西": {
        4: {"goods": ["弹丸加速装置"], "param": 0.2},
        5: {"goods": ["弹丸加速装置"], "param": 0.1},
    },
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
        4: {"goods": ["拼装 模型"], "param": 0.2},
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
    "隼": {
        1: {"goods": ["发动机"], "param": 0.2},
        4: {"goods": ["弹丸加速装置", "发动机", "沃德烤鸡", "红茶"], "param": -0.005},
        5: {"goods": ["斑节虾", "人工晶花", "桦石发财树", "石墨烯"], "param": -0.005},
    },
    "奈弥": {
        1: {"goods": ["金箔酒"], "param": 0.2},
        5: {"goods": ["金箔酒"], "param": 0.1},
    },
    "伊尔": {
        1: {"goods": ["阿妮塔101民用无人机"], "param": 0.2},
        5: {"goods": ["阿妮塔101民用无人机"], "param": 0.1},
    },
    "卡洛琳": {
        4: {"goods": ["石墨烯"], "param": 0.2},
        5: {"goods": ["石墨烯"], "param": 0.1},
    },
}
config = config_model.running_business.model_copy()

for role_name, role_level in config.skill_level:
    role_skill_data = skill_data.get(role_name, [])

    for skill_affect in role_skill_data:
        if role_level >= int(skill_affect):
            goods, param = (
                role_skill_data[skill_affect]["goods"],
                role_skill_data[skill_affect]["param"],
            )

            for good_name in goods:
                if good_name not in config.goods_addition:
                    config.goods_addition[good_name] = param
                else:
                    config.goods_addition[good_name] += param

max_book = 10
message = "暂无"


def get_city_data_by_city_level(
    city_level_: RunningBusinessModel.CityLevelModel,
) -> Dict[str, RunningBusinessModel.CityDataModel]:
    city_level_data = {}
    for attached_name, city_name in attached_to_city_data.items():
        city_level = city_level_.model_dump(by_alias=True)
        if city_name not in city_level.keys():
            continue
        level = city_level[city_name] + 1
        city_level_data[attached_name] = RunningBusinessModel.CityDataModel.model_validate(
            city_data[city_name][level]
        )
    return city_level_data


config.city_data = get_city_data_by_city_level(config.city_level)


class SHOP:
    def __init__(self, goods_data: GoodsModel) -> None:
        self.goods_data = goods_data
        self.buy_goods = self.goods_data.buy_goods
        """城市可购买的商品信息"""
        self.sell_goods = self.goods_data.sell_goods
        """城市可出售的商品信息"""
        self.config = config
        """配置信息"""

    def set_buy_goods(
        self,
        city_name: str,
        target: TargetGoodModel,
        type_: Literal["go", "sell"] = "go",
    ):
        """
        说明:
            设置购买商品的信息
        参数:
            :param city_name: 城市名称
            :param target: 目标数据
            :param type_: 类型 go/back
        """
        buy_city_goods = self.buy_goods[city_name]
        for good_name, good_data in buy_city_goods.items():
            if target.num < config.max_goods_num:
                buy_num = config.city_data.get(
                    city_name, RunningBusinessModel.CityDataModel()
                ).buy_num
                skill_num = config.goods_addition.get(
                    good_name, 0
                )  # 角色技能增加的数量
                num = min(
                    round5(good_data.num * (1 + buy_num + skill_num)),
                    config.max_goods_num - target.num,
                )  # 确保购买数量不超过最大商品数量
                price = round5(
                    good_data.price  # 砍价前的价格
                    * (
                        1
                        - getattr(
                            config, type_, RunningBusinessModel.GoBackModel()
                        ).cut_price.percentage
                    )
                )  # 砍价后的价格

                # 检查商品是否已经在target.goods_data中
                if good_name not in target.goods_data:
                    target.goods_data[good_name] = TargetGoodModel.GoodsData(
                        num=0, price=0
                    )

                target.goods_data[good_name].num += num
                # 更新价格时考虑到可能存在多个来源的同一商品，这里仅采用了最后一次计算的价格
                target.goods_data[good_name].price = price

                if buy_city_goods[good_name].isSpeciality:
                    # 特产利润，计算总购买价
                    target.num += num
                    target.price += price * num

        return target

    def get_goods_profit(
        self,
        sell_city_goods: Dict[str, GoodModel],
        buy_city_goods: Dict[str, GoodModel],
        goods_data: Dict[str, TargetGoodModel.GoodsData],
        sell_city_name: str,
        type_: Literal["gp", "back"] = "go",
    ) -> Tuple[int, int, Dict[str, int], Dict[str, TargetGoodModel.GoodsData]]:
        """
        说明:
            获取所有商品的利润
        参数:
            :param sell_city_goods: 出售城市的商品数据
            :param buy_city_goods: 购买城市的商品数据
            :param goods_data: 待购的商品数据
            :param sell_city_name: 出售城市名称
            :param type_: 列车方向 go/back
        返回:
            :return: 总卖价, 总利润, 非特产利润, 特产商品数据
        """
        sell_price = 0  # 总卖价
        profit = 0  # 总利润
        normal_goods = {}  # 非特产利润
        speciality_goods = {}  # 特产商品数据
        for good_name, good_data in goods_data.items():
            # 跳过不存在的商品
            if good_name not in sell_city_goods:
                continue
            num = good_data.num
            buy_price = good_data.price  # 购买价格
            old_no_revenue_sell_price = sell_city_goods[
                good_name
            ].price  # 不带税的售价，砍抬前
            # 不带税的售价
            no_revenue_sell_price = round5(
                old_no_revenue_sell_price
                * (
                    1
                    + getattr(
                        config, type_, RunningBusinessModel.GoBackModel()
                    ).raise_price.percentage
                )
            )
            tax_rate = config.city_data[sell_city_name].revenue  # 税率
            no_tax_rate_price = (
                no_revenue_sell_price - buy_price
            ) * num  # 不带税的利润
            revenue = (no_revenue_sell_price - buy_price) * tax_rate  # 税收
            profit += no_tax_rate_price  # 利润

            if not buy_city_goods[good_name].isSpeciality:
                # 低价值商品利润
                normal_goods[good_name] = round5(
                    (no_revenue_sell_price - revenue) * num
                )
            else:
                speciality_goods[good_name] = good_data
                # 高价值商品利润，添加到总利润里
                sell_price += round5((no_revenue_sell_price - revenue) * num)
        return sell_price, profit, normal_goods, speciality_goods

    def get_route_profit(self, type_="go"):
        """
        说明:
            获取路线利润
        参数:
            :param user_data: 用户数据
            :param max_book: 最大进货书数量
            :param type_: 列车方向 go/back
            :return: 路线数据
        """
        routes: RoutesModel = RoutesModel()
        for buy_city_name, buy_city_goods in self.buy_goods.items():
            target = TargetGoodModel()
            # 购买基础量，不带书
            target = self.set_buy_goods(buy_city_name, target, type_)
            while target.num < config.max_goods_num: # 直到货仓被装满
                target.book += 1
                target = self.set_buy_goods(buy_city_name, target, type_)

            for sell_city_name, sell_city_goods in self.sell_goods.items():
                # 跳过同城市和不存在的城市
                if (
                    buy_city_name == sell_city_name
                    or sell_city_name not in config.city_data
                    or buy_city_name not in config.city_data
                ):
                    # print(f"buy_city_name: {buy_city_name}, sell_city_name: {sell_city_name}")
                    continue
                sell_price, profit, normal_goods, speciality_goods = self.get_goods_profit(
                    sell_city_goods,
                    buy_city_goods,
                    target.goods_data,
                    sell_city_name,
                    type_,
                )

                tax_rate = config.city_data[buy_city_name].revenue  # 税率
                # 总疲劳
                city_tired = (
                    city_tired_data.get(f"{buy_city_name}-{sell_city_name}", 99999)
                    + getattr(config, type_, RunningBusinessModel.GoBackModel()).raise_price.profit
                    + getattr(config, type_, RunningBusinessModel.GoBackModel()).cut_price.profit
                )

                tired_profit = round5(profit / city_tired)  # 单位疲劳
                book_profit = (
                    0 if target.book == 0 else round5(profit / target.book)
                )  # 单书利润
                buy_price = round5(target.price * (1 + tax_rate))  # 总买价

                routes.root.append(
                    RouteModel(
                        buy_city_name=buy_city_name,
                        sell_city_name=sell_city_name,
                        tax_rate=tax_rate,
                        buy_price=buy_price,
                        sell_price=sell_price,
                        city_tired=city_tired,
                        profit=profit,
                        tired_profit=tired_profit,
                        book_profit=book_profit,
                        book=target.book,
                        num=target.num,
                        goods_data=speciality_goods,
                    )
                )

        return routes

    def get_book_routes_by_city_name(
        self,
        book_routes: List[RouteModel],
        buy_city_name: str,
        sell_city_name: str,
        book: int,
    ):
        """
        说明:
            通过城市名称获取单位疲劳最高的书本路线
        参数:
            :param book_routes: 书本路线
            :param buy_city_name: 购买城市名称
            :param sell_city_name: 出售城市名称
            :param book: 书本数量
        """
        return max(
            (
                route
                for route in book_routes
                if route.buy_city_name == buy_city_name
                and route.sell_city_name == sell_city_name
                and route.book <= 10 - book
            ),
            key=lambda obj: obj.tired_profit,
            default=RouteModel(),
        )

    def get_optimal_route(self) -> Tuple[RouteModel, RouteModel, int]:
        """
        说明:
            获取往返路线的最优路线
        """
        # TODO 也许需要改成异步
        routes = self.get_route_profit("back")
        optimal_route: Tuple[RouteModel, RouteModel, int]  = (RouteModel(), RouteModel(), 0)
        set_go_city: List[Tuple[str, str]] = []
        for go_route in routes:
            if (go_route.buy_city_name, go_route.sell_city_name) in set_go_city:
                continue
            set_go_city.append((go_route.sell_city_name, go_route.buy_city_name))
            back_route = routes.find(buy_city_name=go_route.sell_city_name, sell_city_name=go_route.buy_city_name)
            if back_route is not None:
                profit = go_route.profit + back_route.profit
                city_tired = go_route.city_tired + back_route.city_tired
                tired_profit = round5(profit / city_tired)
                if tired_profit > optimal_route[2]:
                    optimal_route = [go_route, back_route, tired_profit]

        return optimal_route

    def show(self, route: Tuple[RouteModel, RouteModel]):
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
        book_profit = round5(profit / book)
        message = f"""{route[0].buy_city_name}<->{route[0].sell_city_name}:
{route[0].buy_city_name}:
    商品数量: {to_goods_num}
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
