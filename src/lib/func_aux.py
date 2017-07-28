from locale import *
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt


def str_to_float(sValue):
	setlocale(LC_NUMERIC, '')
	value = atof(sValue)
	return value


def paint_row(item, profit, result=None):
	profit = str_to_float(profit)
	if result == "Pendiente":
		for j in range(18):
			item.setBackground(j, QBrush(Qt.yellow))
	else:
		if profit < 0:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.red))
		elif profit > 0:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.green))
		else:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.cyan))

	return item


def key_from_value(dic, value):
	key = list(dic.keys())[list(dic.values()).index(value)]
	return key

def str_to_bool(s):
	if s == 'True':
		return True
	else:
		return False

def numberToMonth(index):
	month = {
		1: "Enero",
		2: "Febrero",
		3: "Marzo",
		4: "Abril",
		5: "Mayo",
		6: "Junio",
		7: "Julio",
		8: "Agosto",
		9: "Septiembre",
		10: "Octubre",
		11: "Noviembre",
		12: "Diciembre"
	}[index]

	return month



