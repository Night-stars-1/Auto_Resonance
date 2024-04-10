# TODO: 1.数据模型化 2.提高可读性

import json
from decimal import Decimal, ROUND_HALF_UP
import time
from typing import Dict, List, Literal
from ..models.goods import GoodModel, GoodsModel
from ..models.srap import SrapRequestModel
from ..models.config import UserModel, config as config_model

def round5(x):
    return int(Decimal(x).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

with open("resources/goods/CityGoodsData.json", "r", encoding="utf-8") as file:
    city_goods_data = json.load(file)

with open("resources/goods/CityData.json", "r", encoding="utf-8") as file:
    city_data = json.load(file)

with open("resources/goods/AttachedToCityData.json", "r", encoding="utf-8") as file:
    attached_to_city_data: dict = json.load(file)

with open("resources/goods/CityTiredData.json", "r", encoding="utf-8") as file:
    city_tired_data = json.load(file)

skill_data = {
    "朱利安": {1: {"goods": ["斑节虾"], "param": 0.2}},
    "狮鬃": {1: {"goods": ["荧光棒"], "param": 0.2}, 4: {"goods": ["扬声器"], "param": 0.2}},
    "魇": {1: {"goods": ["刀具"], "param": 0.2}, 5: {"goods": ["刀具"], "param": 0.1}},
    "塞西尔": {4: {"goods": ["香水"], "param": 0.2}, 5: {"goods": ["香水"], "param": 0.3}},
    "雷火": {4: {"goods": ["曼德工具箱"], "param": 0.2}},
    "黛丝莉": {4: {"goods": ["毛绒玩具"], "param": 0.2}, 5: {"goods": ["毛绒玩具"], "param": 0.1}},
    "艾略特": {4: {"goods": ["游戏卡带", "游戏机"], "param": 0.2}},
    "多萝西": {4: {"goods": ["弹丸加速装置"], "param": 0.2}, 5: {"goods": ["弹丸加速装置"], "param": 0.1}},
    "星花": {1: {"goods": ["人工晶花"], "param": 0.2}},
    "瑞秋": {4: {"goods": ["医药品"], "param": 0.2}},
    "菲妮娅": {4: {"goods": ["大龙虾"], "param": 0.2}, 5: {"goods": ["大龙虾"], "param": 0.1}},
    "瓦伦汀": {4: {"goods": ["学会书籍"], "param": 0.2}, 5: {"goods": ["学会书籍"], "param": 0.1}},
    "阿知波": {4: {"goods": ["拼装 模型"], "param": 0.2}, 5: {"goods": ["拼装模型"], "param": 0.1}},
    "闻笙": {4: {"goods": ["限定公仔"], "param": 0.2}, 5: {"goods": ["限定公仔"], "param": 0.1}},
    "山岚": {4: {"goods": ["折扇"], "param": 0.2}},
    "叶珏": {1: {"goods": ["红茶"], "param": 0.2}, 4: {"goods": ["家用太阳能电池组"], "param": 0.2}, 5: {"goods": ["红茶"], "param": 0.1}},
    "隼": {1: {"goods": ["发动机"], "param": 0.2}, 4: {"goods": ["弹丸加速装置", "发动机", "沃德烤鸡", "红茶"], "param": -0.005}, 5: {"goods": ["斑节虾", "人工晶花", "桦石发财树", "石墨烯"], "param": -0.005}},
    "奈弥": {1: {"goods": ["金箔酒"], "param": 0.2}, 5: {"goods": ["金箔酒"], "param": 0.1}},
    "伊尔": {1: {"goods": ["阿妮塔101民用无人机"], "param": 0.2}, 5: {"goods": ["阿妮塔101民用无人机"], "param": 0.1}},
    "卡洛琳": {4: {"goods": ["石墨烯"], "param": 0.2}, 5: {"goods": ["石墨烯"], "param": 0.1}}
}
config = config_model.user.model_copy()

for role_name, role_level in config.skill_level:
    role_skill_data = skill_data.get(role_name, [])

    for skill_affect in role_skill_data:
        if role_level >= int(skill_affect):
            goods, param = role_skill_data[skill_affect]["goods"], role_skill_data[skill_affect]["param"]

            for good_name in goods:
                if good_name not in config.goods_addition:
                    config.goods_addition[good_name] = param
                else:
                    config.goods_addition[good_name] += param

max_book = 10
message = '暂无'

def get_city_data_by_city_level(city_level_: UserModel.CityLevelModel) -> Dict[str, UserModel.CityDataModel]:
    city_level_data = {}
    for attached_name, city_name in attached_to_city_data.items():
        city_level = city_level_.model_dump(by_alias=True)
        if city_name not in city_level.keys():
            continue
        level = city_level[city_name] + 1
        city_level_data[attached_name] = UserModel.CityDataModel.model_validate(city_data[city_name][level])
    return city_level_data


config.city_data = get_city_data_by_city_level(config.city_level)

class SHOP:
    def __init__(self, goods_data: GoodsModel) -> None:
        self.goods_data = goods_data
        self.buy_goods = self.goods_data.speciality_goods
        self.sell_goods = self.goods_data.sell_goods
        self.config = config

    def get_optimal_route(self, max_book: int, type_='go'):
        """
        说明:
            获取路线利润
        参数:
            :param user_data: 用户数据
            :param max_book: 最大书本数量
            :param buy_list: 购买列表
            :param sell_list: 出售列表
            :param type_: 类型 go/back
            :return: 路线数据
        """
        routes = []
        for buy_city_name in self.buy_goods.keys():
            target = {
                'goodsData': {},
                'num': 0,
                'price': 0,
                'book': 0,
                'maxBook': max_book
            }
            # 购买基础量，不带书
            target = self.set_buy_goods(buy_city_name, target, type_)
            while target['num'] < 400 and target['book'] < target['maxBook']:
                target['book'] += 1
                target = self.set_buy_goods(buy_city_name, target, type_)
            
            for sell_city_name, sell_data in self.sell_goods.items():
                if buy_city_name == sell_city_name or sell_city_name not in config.city_data or buy_city_name not in config.city_data:
                    # print(f"buy_city_name: {buy_city_name}, sell_city_name: {sell_city_name}")
                    continue
                sell_price = 0
                profit = 0
                for goods_name, goods_data in target['goodsData'].items():
                    if goods_name not in sell_data:
                        continue
                    num = goods_data['num']
                    buy_price = goods_data['price'] # 购买价格
                    old_no_revenue_sell_price = sell_data[goods_name].price # 不带税的售价，砍抬前
                    no_revenue_sell_price = round5(old_no_revenue_sell_price * (1 + getattr(config, type_, UserModel.GoBackModel()).raise_price.percentage)) # 不带税的售价
                    tax_rate = config.city_data[sell_city_name].revenue # 税率
                    no_tax_rate_price = (no_revenue_sell_price - buy_price) * num # 不带税的利润
                    revenue = (no_revenue_sell_price - buy_price) * tax_rate # 税收
                    profit += no_tax_rate_price # 利润
                    sell_price += round5((no_revenue_sell_price - revenue) * num)

                tax_rate = config.city_data[buy_city_name].revenue
                buy_price = round5(target['price'] * (1 + tax_rate))
                city_tired = (city_tired_data.get(f"{buy_city_name}-{sell_city_name}", 99999) + 
                              getattr(config, type_, UserModel.GoBackModel()).raise_price.profit + getattr(config, type_, UserModel.GoBackModel()).cut_price.profit)
                tired_profit = round5(profit / city_tired)
                book_profit = 0 if target['book'] == 0 else round5(profit / target['book'])
                
                routes.append({
                    'buyCityName': buy_city_name,
                    'sellCityName': sell_city_name,
                    'taxRate': tax_rate,
                    'buyPrice': buy_price,
                    'sellPrice': sell_price,
                    'cityTired': city_tired,
                    'profit': profit,
                    'tiredProfit': tired_profit,
                    'bookProfit': book_profit,
                    'book': target['book'],
                    'num': target['num'],
                    'goodsData': target['goodsData']
                })

        return routes


    def set_buy_goods(self, city_name: str, target, type_: Literal["go", "sell"]='go'):
        """
        说明:
            设置购买商品的信息
        参数:
            :param city_name: 城市名称
            :param target: 目标数据
            :param type_: 类型 go/back
        """
        for good_name, good_data in self.buy_goods[city_name].items():
            if target['num'] < config.max_goods_num:
                buy_num = config.city_data.get(city_name, UserModel.CityDataModel()).buy_num
                skill_num = config.goods_addition.get(good_name, 0)  # 使用 get 方法处理默认值
                old_num = round5(good_data.num * (1 + buy_num + skill_num))
                num = min(old_num, config.max_goods_num - target['num'])  # 确保不超过最大商品数量
                old_price = good_data.price
                price = round5(old_price * (1 - getattr(config, type_, UserModel.GoBackModel()).cut_price.percentage))

                # 检查商品是否已经在target['goodsData']中
                if good_name not in target['goodsData']:
                    target['goodsData'][good_name] = {'num': 0, 'price': 0}
                
                target['goodsData'][good_name]['num'] += num
                # 更新价格时考虑到可能存在多个来源的同一商品，这里仅采用了最后一次计算的价格
                target['goodsData'][good_name]['price'] = price
                target['num'] += num
                target['price'] += price * num

        return target


    def get_book_routes_by_city_name(self, book_routes, buy_city_name, sell_city_name, book):
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
            (route for route in book_routes if route['buyCityName'] == buy_city_name and route['sellCityName'] == sell_city_name and route['book'] <= 10 - book),
            key=lambda obj: obj['tiredProfit'],
            default=[]
        )

    def get_go_back_optimal_route_by_tired_profit(self):
        """
        说明:
            获取往返路线的最优路线
        """
        book_profits = []
        book_routes = []

        # 假设 maxBook 已经在外部定义或作为参数传入
        global max_book  # 如果max_book是全局变量，或者将其作为函数参数
        # TODO 也许需要改成异步
        for book in range(max_book - 1):
            book_routes.extend(self.get_optimal_route(book, 'back'))
        for book in range(max_book - 1):
            routes = self.get_optimal_route(book, 'go')
            if not routes:
                continue
            route = max(routes, key=lambda obj: obj['bookProfit'] + 
                        self.get_book_routes_by_city_name(book_routes, obj['sellCityName'], obj['buyCityName'], obj['book'])['bookProfit'])
            paired_route = self.get_book_routes_by_city_name(book_routes, route['sellCityName'], route['buyCityName'], route['book'])
            book_profits.append((route, paired_route))

        benchmark_profit = sum(item[0]['bookProfit'] + item[1]['bookProfit'] for item in book_profits) / len(book_profits)

        optimal_route = max(book_profits, key=lambda obj: (obj[0]['tiredProfit'] + obj[1]['tiredProfit'] > benchmark_profit))
        optimal_route = max(
            (obj for obj in book_profits if sum(o['bookProfit'] for o in obj) > benchmark_profit),
            key=lambda obj: sum(o['tiredProfit'] for o in obj),
            default=None  # 如果没有符合条件的对象，返回None
        )

        return self.show(optimal_route)

    def show(self, route):
        to_goods_num = ','.join([f"{name}{route[0]['goodsData'][name]['num']}" for name in route[0]['goodsData']])
        back_goods_num = ','.join([f"{name}{route[1]['goodsData'][name]['num']}" for name in route[1]['goodsData']])
    
        message = f"""{route[0]['buyCityName']}<->{route[0]['sellCityName']}:
{route[0]['buyCityName']}:
    商品数量: {to_goods_num}
    商品总量: {route[0]['num']}
    购买价格: {route[0]['buyPrice']}
    出售价格: {route[0]['sellPrice']}
    商品利润: {route[0]['profit']}
    所需疲劳: {route[0]['cityTired']}
    疲劳利润: {route[0]['tiredProfit']}
    单书利润: {route[0]['bookProfit']}
    书本数量: {route[0]['book']}
{route[0]['sellCityName']}:
    商品数量: {back_goods_num}
    商品总量: {route[1]['num']}
    购买价格: {route[1]['buyPrice']}
    出售价格: {route[1]['sellPrice']}
    商品利润: {route[1]['profit']}
    所需疲劳: {route[1]['cityTired']}
    疲劳利润: {route[1]['tiredProfit']}
    单书利润: {route[1]['bookProfit']}
    书本数量: {route[1]['book']}
总计:
    利润: {route[0]['profit'] + route[1]['profit']}
    所需疲劳: {route[0]['cityTired'] + route[1]['cityTired']}
    疲劳利润: {route[0]['tiredProfit'] + route[1]['tiredProfit']}
    单书利润: {route[0]['bookProfit'] + route[1]['bookProfit']}
    书本数量: {route[0]['book'] + route[1]['book']}"""
    
        return message
