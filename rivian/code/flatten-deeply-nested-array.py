from typing import Union

NestedArray = Union[int, list]


def flatten(arr: list[NestedArray], n: int) -> list[NestedArray]:
    if n == 0:
        return arr

    flattenList = []

    def do_flatten(items, times):
        for item in items:
            if isinstance(item, list) and times > 0:
                do_flatten(item, times - 1)
            else:
                flattenList.append(item)

    do_flatten(arr, n)
    return flattenList