import sys, sqlite3, os, inspect, json, yaml
from os.path import expanduser
from collections import OrderedDict


class LibYaml:
	def __init__(self, directory=expanduser("~/.betcon/config.yml")):
		self.directory = directory
		config = self.load()
		self.stake = config["stake"]

	def load(self):
		if not os.path.exists(self.directory):
			self.initConfig()

		stream = open(self.directory, 'r')
		config = yaml.load(stream)
		stream.close()
		return config

	def initConfig(self):
		data = {'stake': {'porcentage': 1.0, 'stake': 0, 'type': 1}}

		stream = open(self.directory, 'w')
		yaml.dump(data, stream, default_flow_style=False)
		stream.close()




