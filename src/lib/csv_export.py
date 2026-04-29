import csv
from os.path import expanduser
from bbdd import Bbdd


class CsvExport:
	def __init__(self, directory=expanduser("~/betcon.csv"), directory_bd=None, progress_callback=None):
		self.directory = directory
		self.directory_bd = directory_bd
		self.progress_callback = progress_callback

	def export(self):
		if self.directory_bd is None:
			bd = Bbdd()
		else:
			bd = Bbdd(self.directory_bd)

		data = bd.select("bet")
		dataCsv = [["Fecha", "Deporte", "Competicion", "Región", "Local", "Visitante", "Pick", "Casa", "Mercado",
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
			dataCsv.append(row)

		bd.close()
		
		# Escribir archivo CSV
		with open(self.directory, 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(dataCsv)

	def count_rows(self):
		with open(self.directory, 'r', encoding='utf-8') as csvfile:
			return sum(1 for row in csv.reader(csvfile) if row and row[0] != 'Fecha')

	def imports(self):
		if self.directory_bd is None:
			bd = Bbdd()
		else:
			bd = Bbdd(self.directory_bd)

		try:
			# Leer archivo CSV
			with open(self.directory, 'r', encoding='utf-8') as csvfile:
				reader = csv.reader(csvfile)
				data = list(reader)

			imported = 0
			for i in data:
				row = []
				if i[0] == "Fecha":
					continue
				row.append(i[0])
				sport = bd.getId(i[1], "sport")
				if sport is None:
					bd.insert(["name"], [i[1]], "sport")
					sport = bd.getId(i[1], "sport")
				row.append(sport)

				region = bd.getId(i[3], "region")
				if region is None:
					bd.insert(["name"], [i[3]], "region")
					region = bd.getId(i[3], "region")

				competition = bd.getId(i[2], "competition")
				if competition is None:
					bd.insert(["name", "region", "sport"], [i[2], region, sport], "competition")
					competition = bd.getId(i[2], "competition")
				row.append(competition)
				row.append(region)

				row.append(i[4])
				row.append(i[5])
				row.append(i[6])

				bookie = bd.getId(i[7], "bookie")
				if bookie is None:
					bd.insert(["name"], [i[7]], "bookie")
					bookie = bd.getId(i[7], "bookie")
				row.append(bookie)

				market = bd.getId(i[8], "market")
				if market is None:
					bd.insert(["name"], [i[8]], "market")
					market = bd.getId(i[8], "market")
				row.append(market)

				tipster = bd.getId(i[9], "tipster")
				if tipster is None:
					bd.insert(["name"], [i[9]], "tipster")
					tipster = bd.getId(i[9], "tipster")
				row.append(tipster)

				row.append(i[10])
				row.append(i[11])
				row.append(i[12])
				row.append(i[13])
				row.append(i[14])
				row.append(i[15])
				row.append(False if i[16] == "No" else True)

				columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
				           "tipster", "stake", "one", "result", "profit", "bet", "quota", "free"]

				bd.insert(columns, row, "bet")
				imported += 1
				if self.progress_callback:
					self.progress_callback(imported)
		except Exception:
			return "Error de importación: El archivo de importación no tiene una estructura correcta."








