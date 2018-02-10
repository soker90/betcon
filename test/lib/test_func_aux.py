from unittest import TestCase

from hamcrest import assert_that, is_
from src.lib.func_aux import *
from PyQt5.QtWidgets import QTreeWidgetItem
from gettext import gettext as _
import gettext

class TestFuncAux(TestCase):

	gettext.textdomain("betcon")
	gettext.bindtextdomain("betcon", "../lang/mo")

	##################
	# Test paint_row #
	##################

	def test_paint_row_yellow(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)
		item.background(0)

		actual = paint_row(item, "0€", "0")
		assert_that(actual.background(0), is_(QBrush(Qt.yellow)))

		actual = paint_row(item, "-10.0€", "0")
		assert_that(actual.background(0), is_(QBrush(Qt.yellow)))

		actual = paint_row(item, 20.0, "0")
		assert_that(actual.background(0), is_(QBrush(Qt.yellow)))

	def test_paint_row_green(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)

		assert_that(paint_row(item, "0.5€").background(0), is_(QBrush(Qt.green)))
		assert_that(paint_row(item, 10).background(0), is_(QBrush(Qt.green)))

	def test_paint_row_red(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)

		assert_that(paint_row(item, "-10.0€").background(0), is_(QBrush(Qt.red)))
		assert_that(paint_row(item, "-20€").background(0), is_(QBrush(Qt.red)))

	def test_paint_row_cyan(self):
		items = []
		for i in range(18):
			items.append("")

		item = QTreeWidgetItem(items)

		assert_that(paint_row(item, "0€").background(0), is_(QBrush(Qt.cyan)))

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

		assert_that(numberToMonth(1), is_(_("January")))
		assert_that(numberToMonth(2), is_(_("February")))
		assert_that(numberToMonth(3), is_(_("March")))
		assert_that(numberToMonth(4), is_(_("April")))
		assert_that(numberToMonth(5), is_(_("May")))
		assert_that(numberToMonth(6), is_(_("June")))
		assert_that(numberToMonth(7), is_(_("July")))
		assert_that(numberToMonth(8), is_(_("August")))
		assert_that(numberToMonth(9), is_(_("September")))
		assert_that(numberToMonth(10), is_(_("October")))
		assert_that(numberToMonth(11), is_(_("November")))
		assert_that(numberToMonth(12), is_(_("December")))

