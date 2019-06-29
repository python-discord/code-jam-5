"""Module where all functions are being put."""

import math
import random
import json

# temperature-related
def gen_temp_mul(start, end): # generates random multiplier (used in formulas)
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
	if temp.value in range(low, low + quarter):
		t = 0
	elif temp.value in range(high - quarter, high):
		t = 2
	else:
		t = 1
	return t

def fix_temp_rhand(n): # for operations on Temperature objects
	from ..temperature import Temperature as t
	if not isinstance(n, (int, float, t)):
		raise TypeError(f"Unsupported right hand object type for operation with Temperature. Expected instance of (int, float, Temperature).")
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
def rand(low, high):
	return random.randint(low, high)

def fix_inaccuracy(strFloat, n):
	if strFloat.endswith('.99'):
		return math.ceil(n) - (1 if n < 0 else 0) # latter part - to fix ceiling e.g. math.ceil(-27.99) is actually -27
	elif strFloat.endswith('.01'):
		return math.trunc(n)
	return n

def fix_float(n):
	if isinstance(n, float):
		t = "{:.2f}".format(n)
		x = float(t)
		if x.is_integer():
			return int(x)
		else:
			return fix_inaccuracy(t, x)
	return n