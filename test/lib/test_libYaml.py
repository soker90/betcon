# from unittest import TestCase
#
# from hamcrest import assert_that, is_
# from src.lib.libyaml import LibYaml
#
#
# class TestLibYaml(TestCase):
# 	lib = LibYaml("/tmp/test.yml")
#
# 	def test_load(self):
# 		config = {'stake': {'percentage': 1.0, 'stake': 0, 'type': 1}}
#
# 		assert_that(config, self.lib.load())
#
# 	def test_save(self):
# 		valor = {'test': 'valor'}
# 		self.lib.config = valor
# 		self.lib.save()
#
# 		assert_that(valor, self.lib.load())
#
# 	def tearDown(self):
# 		import os
# 		os.remove('/tmp/test.yml')
#
#
#
#
#
#
