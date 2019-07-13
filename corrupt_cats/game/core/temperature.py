from .utils.functions import (
    to_celsius, to_fahrenheit, fix_temp_rhand
)
from .constants import setup

temperature_system = setup.get("temperature_system", "C")


class Temperature:
    def __init__(self, value, system=None):
        self.value = value
        self.system = temperature_system if system is None else system

    def __repr__(self):
        temp = self.to_string()
        ret = f"<temperature: {temp}>"
        return ret

    def __str__(self):
        return self.to_string()

    def to_celsius(self):
        self.value = self.C
        self.system = "C"

    def to_fahrenheit(self):
        self.value = self.F
        self.system = "F"

    def copy(self):
        return Temperature(float("{:.2f}".format(self.value)), self.system)

    @property
    def C(self):
        return self.value if self.isinsystem("C") else to_celsius(self.value)

    @property
    def F(self):
        return self.value if self.isinsystem("F") else to_fahrenheit(self.value)

    def to_string(self):
        return str(self.value) + f"°{self.system}"

    def isinsystem(self, system):
        return self.system == system

    def __eq__(self, other):
        return self.value == fix_temp_rhand(other)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.value > fix_temp_rhand(other)

    def __lt__(self, other):
        return self.value < fix_temp_rhand(other)

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __add__(self, other):
        return self.value + fix_temp_rhand(other)

    def __sub__(self, other):
        return self.value + fix_temp_rhand(other)

    def __mul__(self, other):
        return self.value + fix_temp_rhand(other)

    def __div__(self, other):
        return self.value + fix_temp_rhand(other)

    def __iadd__(self, other):
        self.value += fix_temp_rhand(other)
        return self

    def __isub__(self, other):
        self.value -= fix_temp_rhand(other)
        return self

    def __imul__(self, other):
        self.value *= fix_temp_rhand(other)
        return self

    def __idiv__(self, other):
        self.value /= fix_temp_rhand(other)
        return self
