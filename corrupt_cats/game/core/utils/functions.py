"""Module where all functions are being put."""

import math
import random
import json


# temperature-related
def gen_temp_mul(start, end):  # generates random multiplier (used in formulas)
    return random.randint(start*10, end*10)/10


def to_celsius(fahrenheit_deg):
    base = (fahrenheit_deg-32) * (5/9)
    return fix_float(base)


def to_fahrenheit(celsius_deg):
    base = (9/5) * celsius_deg + 32
    return fix_float(base)


def check_temp(temp, high, low):
    temp_range = high - low
    quarter = temp_range // 4
    if temp.value in range(low, low + quarter):  # if temperature is quite low
        t = 0
    elif temp.value in range(high - quarter, high):  # if temperature is too high
        t = 2
    else:  # if temperature is ok
        t = 1
    return t


def fix_temp_rhand(n):  # for operations on Temperature objects
    from ..temperature import Temperature as t
    if not isinstance(n, (int, float, t)):
        raise TypeError(f"Right-hand operand needs to be instance of (int, float, Temperature).")
    return n.value if isinstance(n, t) else n


# file-related
def load_json(file_path):
    try:
        res = open(file_path).read()
        result = json.loads(res)
    except FileNotFoundError:
        raise UserWarning("'{}' was not found.".format(file_path))
    return result


# misc
def rnd(seq):
    """Generates random index for a sequence"""
    return int(
        random.random()*len(seq)
    )


def int_to_str(number: int):
    """Formats integer to string.
    This function is used for operating with image names.
    Example: int_to_str(2) -> '02'
    """
    # UNUSED
    n = int(number)
    s = str(n)
    return s if len(s) > 1 else ('0' + s)


def get_rand_keys(d):
    r = random.randint(2, len(d))
    keyset = []
    while len(keyset) < r:
        c = random.choice(list(d))
        if c not in keyset:
            keyset.append(c)
    return keyset


def fix_inaccuracy(strFloat, n):
    if strFloat.endswith('.99'):
        return math.ceil(n) - (1 if n < 0 else 0)  # latter fixes ceil; math.ceil(-27.99) is -27
    elif strFloat.endswith('.01'):
        return math.trunc(n)
    return n


def fix_float(n):
    if isinstance(n, float):
        t = "{:.2f}".format(n)  # get truncated float as string, e.g "13.67"
        x = float(t)
        if x.is_integer():
            return int(x)
        else:
            return fix_inaccuracy(t, x)
    return n
