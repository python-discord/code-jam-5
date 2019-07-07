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
    """Pipes the output of a function through a set of functions."""
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
    """From a string name, retrieve the related callable which is expected to be a type converter
    or a constructor of some sort."""
    try:
        type_ = globals()[typename]
    except KeyError:
        raise

    if not callable(type_):
        raise UserWarning("{!r} is not a callable.".format(type_))

    return type_


def flatten(array):
    """Flattens a multi-dimensional iterable."""
    for item in array:
        if (
            isinstance(array, types.GeneratorType) or
            type(array) in (map, filter, iter, list, tuple)
        ):
            yield from item
        else:
            yield item


class both_class_instance:
    """
    Allow a method to apply to both a class object and its instance objects.
    Either will be passed as the first parameter of the method.
    A.do()
    A().do()
    """

    def __init__(self, meth):
        self.meth = meth

    def __get__(self, instance, owner):
        return partial(self.meth, instance or owner)
