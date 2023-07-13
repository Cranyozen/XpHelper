"""经验点 等级 转换工具"""
# Data from https://minecraft.fandom.com/wiki/Experience

# pylint: disable=C0103 # Variable name "xxx" doesn't conform to snake_case naming style

from sympy import Symbol, solve

def get_point_by_level(level: int) -> int:
    """通过经验点获取对应的等级

    Args:
        level (int): 经验点

    Raises:
        ValueError: 未知的等级

    Returns:
        int: 对应的等级
    """
    # Data from https://minecraft.fandom.com/wiki/Experience#Leveling_up
    # point = a * (level ** 2) + b * level + c
    if 0 <= level <= 16:
        a, b, c = 1, 6, 0
    elif 17 <= level <= 31:
        a, b, c = 2.5, -40.5, 360
    elif level >= 32:
        a, b, c = 4.5, -162.5, 2220
    else:
        raise ValueError
    return int (a * (level ** 2) + b * level + c)

def get_require_point_by_level(current_level: int, target_level: int) -> int:
    """获取升级所需的经验值

    Args:
        current_level (int): 当前等级
        target_level (int): 目标等级

    Returns:
        int: 升级所需的经验值 (负数表示减少)
    """
    return get_point_by_level(target_level) - get_point_by_level(current_level)

def get_level_by_point(point: int) -> float:
    """通过等级获取对应的经验点

    Args:
        point (int): 等级

    Raises:
        ValueError: 位置的等级

    Returns:
        float: 对应的经验点
    """
    # point = a * (level ** 2) + b * level + c
    level = Symbol('level', nonnegative=True)
    if 0 <= point <= 352:
        a, b, c = 1, 6, 0
    elif 353 <= point <= 1507:
        a, b, c = 2.5, -40.5, 360
    elif point >= 1508:
        a, b, c = 4.5, -162.5, 2220
    else:
        raise ValueError
    return float(solve(a * (level ** 2) + b * level + c - point, level)[0])
    