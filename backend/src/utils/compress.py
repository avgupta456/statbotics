from typing import List


def compress(arr: List[int]) -> str:
    return "".join([str(x).ljust(5, "0") for x in arr])


def decompress(string: str) -> List[int]:
    return [int(string[i : i + 5]) for i in range(0, len(string), 5)]
