from locale import *
from sre_compile import isstring

from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from gettext import gettext as _
import gettext

gettext.textdomain("betcon")
gettext.bindtextdomain("betcon", "../../lang/mo")

def str_to_float(sValue):
	setlocale(LC_NUMERIC, '')
	value = atof(sValue.replace(',', '.'))
	return value


def paint_row(item, profit, result=None):
	if isstring(profit):
		profit = float(profit[:-1])

	profit = float(profit)
	if result == str(0):
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
		1: _("January"),
		2: _("February"),
		3: _("March"),
		4: _("April"),
		5: _("May"),
		6: _("June"),
		7: _("July"),
		8: _("August"),
		9: _("September"),
		10: _("October"),
		11: _("November"),
		12: _("December")
	}[index]

	return month

def numberToResult(index):

	index = int(index)

	result = {
		0: _("Pending"),
		1: _("Successful"),
		2: _("Failed"),
		3: _("Null"),
		4: _("Half Successful"),
		5: _("Half Failed"),
		6: _("Cash out")
	}[index]

	return result


