from dataclasses import dataclass

from PyQt5.QtCore import pyqtProperty, QObject, pyqtSignal

# https://stackoverflow.com/questions/48425316/how-to-create-pyqt-properties-dynamically


def resolve_type(type_):
    return {
        str: 'QString'
    }.get(type_, type_)


def make_getter_property(name, type_, constant=None, notify=None):

    print(name, '=>', type_)

    type_ = resolve_type(type_)

    kw = {}
    if constant is not None:
        kw['constant'] = constant
    if notify is not None:
        kw['notify'] = notify

    fn = lambda _: getattr(_, name)

    kw['fget'] = fn

    return pyqtProperty(type_, **kw)


import builtins


def dataqobject(cls):

    """
    An attempt to abstract QObject boilerplate for simple data classes.
    """

    old_annotations = cls.__annotations__

    cache = lambda key: '_%s' % key

    # We want the field variables to have a different name, since those 
    # are reserved for getters
    new_annotations = {
        cache(key) : value
        for key, value in old_annotations.items()
    }

    # Default values are actually stored directly in the class namespace
    defaults = {
        key: getattr(cls, key)
        for key in old_annotations
        if hasattr(cls, key)
    }

    new_defaults = {
        cache(key): value
        for key, value in defaults.items()
    }

    class ncls(QObject):

        # def __init__(self, **kw):

        #     QObject.__init__(self)

        #     d = {**defaults}
        #     d.update(kw)

        #     if len(d) != len(old_annotations):
        #         raise UserWarning

        #     for key, value in d.items():
        #         setattr(self, cache(key), value)


        def __post_init__(self):
            QObject.__init__(self)

        x = pyqtProperty('QString', fget=lambda self: self.__class__.__name__)

    ncls.__annotations__ = new_annotations

    ncls = dataclass(ncls)

    # Build default annotations
    for key, value in new_defaults.items():
        setattr(ncls, key, value)

    # Build signals
    signals = {}
    for key in old_annotations:
        signal = pyqtSignal()
        signals[key] = signal
        key = '%sChanged' % key
        setattr(ncls, key, signal)
        print(getattr(ncls, key))

    # Build getters
    for key, type_ in old_annotations.items():
        setattr(
            ncls,
            key, 
            pyqtProperty(
                resolve_type(type_), 
                notify=signals[key], 
                fget=lambda _: getattr(_, cache(key))
            )
        )

    return ncls