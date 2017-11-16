from unittest import TestCase

from hamcrest import assert_that, is_
from src.lib.func_aux import *
from PyQt5.QtWidgets import QTreeWidgetItem

class TestFuncAux(TestCase):

	#####################
	# Test str_to_float #
	#####################

	def test_str_to_float21(self):
		value = 2.1
		sValue = "2,1"

		assert_that(str_to_float(sValue), is_(value))

	def test_str_to_float_4decimal(self):
		value = 10.3333
		sValue = "10,3333"

		assert_that(str_to_float(sValue), is_(value))

	def test_str_to_float_only_decimal(self):
		value = 0.450
		sValue = "0,450"

		assert_that(str_to_float(sValue), is_(value))

	##################
	# Test paint_row #
	##################

	def test_paint_row_yellow(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)
		item.background(0)

		actual = paint_row(item, "0", "Pendiente")
		assert_that(actual.background(0), is_(QBrush(Qt.yellow)))

		actual = paint_row(item, "-10.0", "Pendiente")
		assert_that(actual.background(0), is_(QBrush(Qt.yellow)))

		actual = paint_row(item, "20.0", "Pendiente")
		assert_that(actual.background(0), is_(QBrush(Qt.yellow)))

	def test_paint_row_green(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)

		assert_that(paint_row(item, "0,5").background(0), is_(QBrush(Qt.green)))
		assert_that(paint_row(item, "10").background(0), is_(QBrush(Qt.green)))

	def test_paint_row_red(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)

		assert_that(paint_row(item, "-10.0").background(0), is_(QBrush(Qt.red)))
		assert_that(paint_row(item, "-20").background(0), is_(QBrush(Qt.red)))

	def test_paint_row_cyan(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)

		assert_that(paint_row(item, "0").background(0), is_(QBrush(Qt.cyan)))

	#######################
	# Test key_from_value #
	#######################

	def test_key_from_value(self):
		dic = {1: 3, 2: 22, "ss": "ss", 43: "jj"}

		value = 22

		assert_that(key_from_value(dic, value), is_(2))

	####################
	# Test str_to_bool #
	####################

	def test_str_to_bool(self):

		assert_that(str_to_bool("True"), is_(True))
		assert_that(str_to_bool("False"), is_(False))

	######################
	# Test numberToMonth #
	######################

	def test_numberToMonth(self):

		assert_that(numberToMonth(1), is_("Enero"))
		assert_that(numberToMonth(2), is_("Febrero"))
		assert_that(numberToMonth(3), is_("Marzo"))
		assert_that(numberToMonth(4), is_("Abril"))
		assert_that(numberToMonth(5), is_("Mayo"))
		assert_that(numberToMonth(6), is_("Junio"))
		assert_that(numberToMonth(7), is_("Julio"))
		assert_that(numberToMonth(8), is_("Agosto"))
		assert_that(numberToMonth(9), is_("Septiembre"))
		assert_that(numberToMonth(10), is_("Octubre"))
		assert_that(numberToMonth(11), is_("Noviembre"))
		assert_that(numberToMonth(12), is_("Diciembre"))

