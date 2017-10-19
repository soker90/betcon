from unittest import TestCase

from hamcrest import assert_that, is_
from src.lib.libyaml import LibYaml
from os.path import expanduser
from pyexcel_ods import save_data, get_data
from collections import OrderedDict
from src.lib.bbdd import Bbdd
from src.lib.ods import Ods


class TestOds(TestCase):
	db = Ods("/tmp/tmp.ods")

	def test_export(self):
		dataOds = [["Fecha", "Deporte", "Competicion", "Región", "Local", "Visitante", "Pick", "Casa", "Mercado",
		            "Tipster", "Stake", "Unidad", "Resultado", "Beneficio", "Apuesta", "Cuota", "Gratuita"]
		           ["1", "2", "3", "4", "5", "6", "7", "8","9", "10", "11", "12", "13", "14", "15", "16", "17"]
		           ]

		assert_that(config, self.lib.load())

	def tearDown(self):
		import os
		os.remove('/tmp/tmp.ods')






