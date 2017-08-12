import sys, sqlite3, os, inspect
from os.path import expanduser
from pyexcel_ods import save_data
from collections import OrderedDict
from bbdd import Bbdd


class Ods:
	def __init__(self, directory=expanduser("~/betcon.ods")):
		self.directory = directory

	def export(self):
		bd = Bbdd()
		file = OrderedDict()
		data = bd.select("bet")
		dataOds = [["Fecha", "Deporte", "Competicion", "Región", "Local", "Visitante", "Pick", "Casa", "Mercado",
		            "Tipster", "Stake", "Unidad", "Resultado", "Beneficio", "Apuesta", "Cuota", "Gratuita"]]
		for i in data:
			row = []
			row.append(i[1])
			row.append(bd.getValue(i[2], "sport"))
			row.append(bd.getValue(i[3], "competition"))
			row.append(bd.getValue(i[4], "region"))
			row.append(i[5])
			row.append(i[6])
			row.append(i[7])
			row.append(bd.getValue(i[8], "bookie"))
			row.append(bd.getValue(i[9], "market"))
			row.append(bd.getValue(i[10], "tipster"))
			row.append(i[11])
			row.append(i[12])
			row.append(i[13])
			row.append(i[14])
			row.append(i[15])
			row.append(i[16])
			row.append("No" if i[17] == 0 else "Sí")
			dataOds.append(row)

		bd.close()
		file.update({"Apuestas": dataOds})

		save_data(self.directory, file)




