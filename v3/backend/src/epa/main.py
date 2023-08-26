# TUNABLE PARAMETERS


def k_func(year: int) -> float:
    return -5 / 8 if year >= 2008 else -5 / 12


def percent_func(year: int, x: int) -> float:
    if year <= 2010:
        return 0.3
    return min(0.5, max(0.3, 0.5 - 0.2 / 6 * (x - 6)))
