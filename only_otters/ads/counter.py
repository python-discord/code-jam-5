import re
import time
from typing import Union


"""
Compute the offset to apply on trigger.
"""


def get_precision(num: Union[int, float]) -> int:
    """Returns the precision of a number."""
    if type(num) == int:
        return 0
    return len(str(num).split('.')[1])


def raw(num: Union[int, float]) -> int:
    """Returns the full count of units in a number.
    33.34 => 3334, 2.00065 => 200065, etc."""
    num = '%.100f' % num
    num = re.sub('0+$', '', num)
    num = num.replace('.', '')
    num = int(num)
    return num


def counter(
    start: Union[int, float], 
    offset: Union[int, float], 
    per: int = 1000, 
    mininterval: int = 1
) -> (float, float):
    """
    Compute the minimum offset and delay that can be achieved given the initial increase value and
    starting value. This is used to build a counter with an increase value as tiny as possible, as
    to make the updating process as sleek as possible to the eye.
    """
    offset_sign = offset > 0 or -1
    offset = abs(offset)
    ofraw = raw(offset)

    if ofraw > per / mininterval:
        return (
            offset_sign * offset / (per / mininterval),
            mininterval / per
        )

    else:
        return (
            offset_sign * offset / ofraw,  # .5 /  5 => .1
            per / ofraw / per  # 1000 / 5 => 200 ; / 1000 => 0.2
        )


if __name__ == "__main__":

    start = 35530.33

    precision = get_precision(start)

    offset, interval = counter(start, -5554.4)
    print(offset, 'per', interval, 'seconds')

    gen = (
        '%.{}f'.format(precision) % (start + offset * _)
        for _ in range(0xffff)
    )

    for i in gen:
        print(i, end='\r')
        time.sleep(interval)
