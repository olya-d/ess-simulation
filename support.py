import random
import math


def greatest_pair_of_factors(n):
    """
    Finds pair of integers (a, b) such as a*b = n and
    there is no such (c, d) that c*d=n and |c-d| < |a-b|.
    It basically finds the closest integer representation of square root.
    Examples:
    greatest_pair_of_factors(5) >> (1, 5)
    greatest_pair_of_factors(20) >> (4, 5)
    """
    pairs = []
    factor = 1
    while factor * factor <= n:
        if n % factor == 0:
            pairs.append((n / factor, factor))
        factor += 1
    greatest = pairs[0]
    for pair in pairs:
        if abs(pair[0] - pair[1]) < abs(greatest[0] - greatest[1]):
            greatest = pair
    return greatest


def distance(x1, y1, x2, y2):
    """
    Return distance^2 between points (x1, y1) and (x2, y2)
    """
    dx = x1 - x2
    dy = y1 - y2
    return dx*dx + dy*dy


def calculate_new_point_in_random_direction(x, y, speed):
    """
    Returns new point (x, y)
    """
    angle = random.random()*360
    return speed*math.cos(math.radians(angle)) + x, speed*math.sin(math.radians(angle)) + y
