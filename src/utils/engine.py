import math
import time


def get_distance(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return math.sqrt(x ** 2 + y ** 2)


def get_ms_per_frame(fps):
    return 10000 / fps


def get_ts():
    return int(round(time.time() * 1000))


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p[0]), int(p[1] + 600)
