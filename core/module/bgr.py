from typing import List, Tuple, Union


def compare_ranges(
    low: Union["BGR", Tuple[int, int, int], List[int]],
    x: Union["BGR", Tuple[int, int, int], List[int]],
    high: Union["BGR", Tuple[int, int, int], List[int]],
    check_self: bool = True
):
    """
    判断指定颜色是否在范围

    :param low: 最低颜色
    :param x: 目标颜色
    :param high: 最高颜色
    :param check_self: 是否检查自己
    """
    low_0, low_1, low_2 = low
    x_0, x_1, x_2 = x
    high_0, high_1, high_2 = high

    if check_self:
        return (
            (low_0 <= x_0 <= high_0)
            and (low_1 <= x_1 <= high_1)
            and (low_2 <= x_2 <= high_2)
        )
    else:
        return (
            (low_0 < x_0 < high_0)
            and (low_1 < x_1 < high_1)
            and (low_2 < x_2 < high_2)
        )


class BGR:
    """BGR 模块"""

    def __init__(self, b: int, g: int, r: int, offset: int = 5):
        self.b = b
        self.g = g
        self.r = r
        self.offset = offset

    def __str__(self):
        return f"B: {self.b}, G: {self.g}, R: {self.r}, O: {self.offset}"

    def __repr__(self):
        return f"BGR({self.b}, {self.g}, {self.r}, O: {self.offset})"

    def __eq__(self, other: Union["BGR", Tuple[int, int, int], List[int]]):
        """
        判断指定BGR是否在范围
        
        :param other: 另一个 BGR
        :warning: 该方法会根据 offset 对前一个 BGR 进行范围偏移
        """
        return compare_ranges(
            (self.b - self.offset, self.g - self.offset, self.r - self.offset),
            other,
            (self.b + self.offset, self.g + self.offset, self.r + self.offset),
        )

    def __ne__(self, other: Union["BGR", Tuple[int, int, int], List[int]]):
        """
        判断指定BGR是否不在范围
        
        :param other: 另一个 BGR
        :warning: 该方法会根据 offset 对前一个 BGR 进行范围偏移
        """
        return not compare_ranges(
            (self.b - self.offset, self.g - self.offset, self.r - self.offset),
            other,
            (self.b + self.offset, self.g + self.offset, self.r + self.offset),
        )
    
    def __le__(self, other: "BGR"):
        return self.b <= other.b and self.g <= other.g and self.r <= other.r

    def __lt__(self, other: "BGR"):
        return compare_ranges(
            (self.b - self.offset, self.g - self.offset, self.r - self.offset),
            other,
            (self.b + self.offset, self.g + self.offset, self.r + self.offset),
            False
        )

    def __iter__(self):
        yield self.b
        yield self.g
        yield self.r

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0 or key == -3:
                return self.r
            elif key == 1 or key == -2:
                return self.g
            elif key == 2 or key == -1:
                return self.b
            else:
                raise IndexError("BGR index out of range")
        else:
            raise TypeError("Invalid index type. Must be an integer.")
