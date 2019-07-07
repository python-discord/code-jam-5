"""
This module is used a central access point for all Qt classes and values.
"""

import PyQt5.Qt as QtBase
from PyQt5.Qt import *  # noqa
from PyQt5.Qt import Qt as constants

__all__ = [
    'constants',
    *dir(QtBase),
]
