import sys, os
from shutil import copy2
from os.path import expanduser

from bbdd import Bbdd

from images import Images


class Bookie:

	ruta = None
	#Setters

	def setId(self, id):
		self.id = id
		bd = Bbdd()

		self.name, self.country = bd.select("bookie", None, "id=" + str(self.id), "name, country")[0]

		bd.close()

	def setName(self, name):
		self.name = name

	def setCountry(self, country):
		self.country = country

	def setAll(self, name, country):
		self.setName(name)
		self.setCountry(country)

	def setRuta(self, ruta):
		self.ruta = ruta

	#Métodos auxiliares

	def isEmpty(self):
		if self.name is None:
			return True
		else:
			return False

	# Base de datos
	def insert(self):
		if not self.isEmpty():
			bd = Bbdd()
			msg = bd.insert(["name", "country"], [self.name, self.country], "bookie")
			bd.close()
		else:
			msg = "Faltan datos por introducir"

		return msg

	def update(self):
		if not self.isEmpty():
			bd = Bbdd()
			msg = bd.update(["name", "country"], [self.name, self.country], "bookie", "id="+self.id)
			bd.close()
			if msg != 0:
				msg = "Se ha producido un error al actualizar la BBDD"
			if self.ruta is not None:
				try:
					if not os.path.exists(expanduser("~") + "/.betcon/resources/bookies"):
						os.makedirs(expanduser("~") + "/.betcon/resources/bookies")
					copy2(self.ruta, expanduser("~") + "/.betcon/resources/bookies/" + self.id + ".png")
					img = Images(expanduser("~") + "/.betcon/resources/bookies/" + self.id + ".png")
					img.resize(100, 20)
				except:
					msg = "Imágen incorrecta"
		else:
			msg = "Faltan datos por introducir"
		return msg

	@staticmethod
	def selectAll():
		bd = Bbdd()
		data = bd.select("bookie", "name")

		items = []
		for i in data:
			item = Bookie()
			item.setId(i[0])
			items.append(item)

		bd.close()
		return items

	@staticmethod
	def delete(id):
		bd = Bbdd()
		msg = bd.delete("bookie", id)
		bd.close()
		if msg != 0:
			msg = "Se ha producido un error al actualizar la BBDD"
		return msg

	@staticmethod
	def deleteWhere(table, where):
		bd = Bbdd()
		msg = bd.deleteWhere(table, where)
		bd.close()
		if msg != 0:
			msg = "Se ha producido un error al actualizar la BBDD"
		return msg

	@staticmethod
	def sumAll(where=None):
		bd = Bbdd()
		data = bd.sum("movement", "money", where)
		if where is None:
			profit = bd.sum("bet", "profit")
			data += profit
		elif where[0] == "b":
			profit = bd.sum("bet", "profit", where)
			data += profit

		bd.close()
		return data

	@staticmethod
	def sumBonus(where=None):
		bd = Bbdd()
		if where:
			where = "free='True' and " + where
		else:
			where = "free='True' "

		data = bd.sum("bonus", "money", where)

		bd.close()
		return data
