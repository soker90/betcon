import sys, sqlite3, os, inspect, json, yaml
from os.path import expanduser
from collections import OrderedDict

from func_aux import checkFileExist


class LibYaml:
	def __init__(self, directory=expanduser("~/.betcon/config.yml")):
		self.directory = directory
		checkFileExist(expanduser("~/.betcon"))
		self.config = self.load()
		self.stake = self.config["stake"]
		self.interface = self.config["interface"]

	def load(self):
		if not os.path.exists(self.directory):
			self.initConfig()

		stream = open(self.directory, 'r')
		config = yaml.load(stream)
		stream.close()
		return config

	def initConfig(self):
		data = {'stake': {'percentage': 1.0, 'stake': 0, 'type': 1}, 'interface': {'coin': '€', 'bookieCountry': 'N'}}

		stream = open(self.directory, 'w')
		yaml.dump(data, stream, default_flow_style=False)
		stream.close()

	def save(self):
		stream = open(self.directory, 'w')
		yaml.dump(self.config, stream, default_flow_style=False)
		stream.close()




