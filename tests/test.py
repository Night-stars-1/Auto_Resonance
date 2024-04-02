"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:47:26
LastEditTime: 2024-04-01 23:52:08
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

data = [
    {
        "text": "在休息区的黑月商店购",
        "score": 0.5981383919715881,
        "position": [[424, 10], [582, 10], [582, 26], [424, 26]],
    },
    {
        "text": "今日首次登录",
        "score": 0.8638824820518494,
        "position": [[42, 22], [135, 22], [135, 39], [42, 39]],
    },
    {
        "text": "获得5场战斗胜利",
        "score": 0.6244779229164124,
        "position": [[236, 23], [355, 23], [355, 39], [236, 39]],
    },
    {
        "text": "行驶100KM",
        "score": 0.791918158531189,
        "position": [[667, 23], [751, 23], [751, 39], [667, 39]],
    },
    {
        "text": "买1次桦石",
        "score": 0.9982701539993286,
        "position": [[464, 33], [539, 33], [539, 53], [464, 53]],
    },
]
centers = {}

for item in data:
    position = item["position"]
    # 计算中心点坐标
    center_x = (position[0][0] + position[2][0]) / 2
    center_y = (position[0][1] + position[2][1]) / 2
    centers[item["text"]] = (center_x, center_y)
    for center, pos in centers.copy().items():
        if abs(center_x - pos[0]) < 50 and pos != (center_x, center_y):
            centers.pop(center)
            if (item["text"] in centers): centers.pop(item["text"])
            centers[center + item["text"]] = (center_x, center_y)

print(centers)
