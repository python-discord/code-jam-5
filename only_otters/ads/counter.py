
import time
import re


"""
Refresh limit is set to 1 ms. (mininterval)
Compute the offset to apply on trigger.
"""


def get_precision(num):
    if type(num) == int:
        return 0
    return len(str(num).split('.')[1])


def raw(num):
    num = '%.100f' % num
    num = re.sub('0+$', '', num)
    num = num.replace('.', '')
    num = int(num)
    return num


def counter(start, offset, per=1000, mininterval=1):

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
