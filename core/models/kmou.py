"""
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2024-04-08 22:18:17
LastEditTime: 2024-04-10 00:42:00
LastEditors: Night-stars-1 nujj1042633805@gmail.com
"""

from typing import Any, Dict, Optional

from .goods import GoodsModel


class KMouRequestModel(GoodsModel):

    def __init__(self, **data) -> None:
        super().__init__(**data)

    @classmethod
    def model_validate(
        self,
        obj: Any,
        strict: Optional[bool] = None,
        from_attributes: Optional[bool] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> GoodsModel:
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
