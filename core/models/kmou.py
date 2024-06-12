"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:18:17
LastEditTime: 2024-06-12 23:43:49
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Any, Dict, Optional, Union

from core.exceptions import StopExecution

from .goods import GoodsModel


class KMouRequestModel(GoodsModel):

    def __init__(self, **data) -> None:
        super().__init__(**data)

    @classmethod
    def model_validate(
        self,
        obj: Union[dict, list],
        strict: Optional[bool] = None,
        from_attributes: Optional[bool] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> GoodsModel:
        if isinstance(obj, dict):
            assert obj.get("error") == None, obj["error"]
        new_obj = []
        for good in obj:
            good["type"] = "sell" if good["type"] == "buy" else "buy"
            new_obj.append(good)
        return super().model_validate(
            {"goods": new_obj},
            strict=strict,
            from_attributes=from_attributes,
            context=context,
        )
