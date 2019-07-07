from functools import wraps, partial
import types


def one_or_many(items: list, default=''):
    """
    Taking a list as input,
    return the first item if there is only one item,
    else return the 'default' value is the list is empty,
    else return the initial list.
    """
    if items:
        if len(items) == 1:
            return items[0]
        return items
    return default


def pipe(*fns):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            r = fn(*a, **kw)
            for f in fns:
                r = f(r)
            return r
        return wrapper
    return decorator


def astype(typename):

    try:
        type_ = globals()[typename]
    except KeyError:
        raise

    if not callable(type_):
        raise UserWarning("{!r} is not a callable.".format(type_))

    return type_


def flatten(array):
    for item in array:
        if (
            isinstance(array, types.GeneratorType) or
            type(array) in (map, filter, iter, list, tuple)
        ):
            yield from item
        else:
            yield item


def exceptprint(*e):

    def decorator(fn, excepts=(Exception,)):

        @wraps(fn)
        def wrapper(*a, **kw):
            try:
                return fn(*a, **kw)
            except excepts as ex:
                print(
                    'e=%s:%s, f=%s, args=%s, kw=%s' % (
                        type(ex).__name__, ex,
                        fn, a, kw
                    )
                )
                raise
        return wrapper

    if len(e) == 1 and not isinstance(e[0], Exception):
        return decorator(e[0])

    return partial(decorator, excepts=e)


class both_class_instance:
    """
    Allow a method to both a class object and its instance objects.
    Either will be passed as the first parameter of the method.
    A.do()
    A().do()
    """

    def __init__(self, meth):
        self.meth = meth

    def __get__(self, instance, owner):
        return partial(self.meth, instance or owner)
