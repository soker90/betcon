import sys, sqlite3, os, inspect, json, yaml
from os.path import expanduser
from collections import OrderedDict


class LibYaml:
	def __init__(self, directory=expanduser("~/.betcon/settings.yaml")):
		self.directory = directory

	def load(self):
		if not os.path.exists(self.directory):
			self.initConfig()

		stream = open(self.directory, 'r')
		config = yaml.load(stream)
		stream.close()

	def initConfig(self):
		stream = open(self.directory, 'w')
		stream.close()




