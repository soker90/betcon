from locale import *


def str_to_float(sValue):
	setlocale(LC_NUMERIC, '')
	value = atof(sValue)
	return value
