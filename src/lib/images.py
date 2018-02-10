import sys, sqlite3, os, inspect, json, yaml
from PIL import Image

class Images:
	def __init__(self, ruta):
		self.ruta = ruta
		self.img = Image.open(self.ruta)

	def resize(self, height, width):
		self.img = self.img.resize((height, width))
		self.img.save(self.ruta)


