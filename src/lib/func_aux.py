import webbrowser
import os
from locale import setlocale, LC_NUMERIC, atof

from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt
from constants import BetResult






def str_to_float(sValue):
	setlocale(LC_NUMERIC, '')
	value = atof(sValue.replace(',', '.'))
	return value


def paint_row(item, profit, result=None):
	if isinstance(profit, str):
		profit = float(profit[:-1])

	profit = float(profit)
	if result is not None and int(result) == BetResult.PENDING:
		for j in range(18):
			item.setBackground(j, QBrush(Qt.GlobalColor.yellow))
	else:
		if profit < 0:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.GlobalColor.red))
		elif profit > 0:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.GlobalColor.green))
		else:
			for j in range(18):
				item.setBackground(j, QBrush(Qt.GlobalColor.cyan))

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

def monthToNumber(index):

	month = {
		_("January"): "01",
		_("February"): "02",
		_("March"): "03",
		_("April"): "04",
		_("May"): "05",
		_("June"): "06",
		_("July"): "07",
		_("August"): "08",
		_("September"): "09",
		_("October"): "10",
		_("November"): "11",
		_("December"): "12"
	}[index]

	return month

def numberToResult(index):

	index = int(index)

	result = {
		BetResult.PENDING:   _("Pending"),
		BetResult.WON:       _("Successful"),
		BetResult.LOST:      _("Failed"),
		BetResult.VOID:      _("Null"),
		BetResult.HALF_WON:  _("Half Successful"),
		BetResult.HALF_LOST: _("Half Failed"),
		BetResult.CASH_OUT:  _("Cash out")
	}[BetResult(index)]

	return result

def openUrl(url):
	webbrowser.open_new_tab(url)

def checkFileExist(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
