import sys
sys.path.append("./lib")
from bbdd import Bbdd

class Bookie:
	#Setters

	def setId(self, id):
		self.id = id
		bd = Bbdd()
		self.name = bd.getValue(self.id, "bookie")
		bd.close()

	def setName(self, name):
		self.name = name

	def setAll(self, name):
		self.setName(name)

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
			msg = bd.insert(["name"], [self.name], "bookie")
			bd.close()
		else:
			msg = "Faltan datos por introducir"

		return msg

	def update(self):
		if not self.isEmpty():
			bd = Bbdd()
			msg = bd.update(["name"], [self.name], "bookie", self.id)
			bd.close()
			if msg != 0:
				msg = "Se ha producido un error al actualizar la BBDD"
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

