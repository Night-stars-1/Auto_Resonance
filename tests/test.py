"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-01 23:47:26
LastEditTime: 2024-04-01 23:52:08
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

data = [
    {
        "text": "您当前的澄明度不足，是否补充澄明度?",
        "score": 0.408284068107605,
        "position": [[37.0, 37.0], [445.0, 37.0], [445.0, 54.0], [37.0, 54.0]],
    },
    {
        "text": "您当前的澄明度不足，是否补充澄明度?",
        "score": 0.408284068107605,
        "position": [[37.0, 37.0], [445.0, 37.0], [445.0, 54.0], [37.0, 54.0]],
    },
]
for item in data:
    if "澄明度不足" in item["text"]:
        print("澄明度不足")
        break
