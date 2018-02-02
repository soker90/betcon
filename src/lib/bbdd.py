import sys, sqlite3, os, inspect, codecs
from os.path import expanduser
from decimal import Decimal


class Bbdd:
	directory = expanduser("~") + "/.betcon/"
	name = "betcon.sqlite3"

	def __init__(self):
		exist = False
		if self.isExist():
			exist = True
		else:
			self.directoryFull = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
			if not os.path.exists(self.directory):
				os.makedirs(self.directory)

		self.bd = sqlite3.connect(self.directory + self.name)
		self.cursor = self.bd.cursor()

		if not exist:
			self.initDatabase()
		else:
			try:
				version = self.select("variable", None, "key = 'version'")[0][1]
				self.updateDatabase(Decimal(version))
			except:
				self.updateDatabase(0)



	def insert(self, columns, values, table):
		aux = ', '.join('?' * len(values))
		if len(columns) == 1:
			columns = '('+str(columns[0])+')'
		else:
			columns = str(tuple(columns))
		query = "INSERT INTO " + table + columns + " VALUES(%s);" % aux
		try:
			self.cursor.execute(query, values)
			self.bd.commit()
		except Exception as e:
			print("Error insert BBDD: {0}".format(e))
			return -1
		return 0

	def update(self, columns, values, table, where=None):

		sentence = " "
		for i in range(len(columns)):
			sentence += str("'" + columns[i]) + "' = '" + str(values[i]) + "', "

		sentence = sentence[:-2]

		query = "UPDATE " + table + " SET " + sentence + " WHERE " + where + ";"
		try:
			self.cursor.execute(query)
			self.bd.commit()
		except Exception as e:
			print("Error update BBDD: {0}".format(e))
			return -1
		return 0

	def delete(self, table, id):
		try:
			self.cursor.execute("DELETE FROM {} WHERE id = ?;".format(table), (id,))
			self.bd.commit()
		except Exception as e:
			print("Error delete BBDD: {0}".format(e))
			return -1
		return 0

	def deleteWhere(self, table, where):
		try:
			query = "DELETE FROM " + table + " WHERE " + where + ";"
			self.cursor.execute(query)
			self.bd.commit()
		except Exception as e:
			print("Error delete BBDD: {0}".format(e))
			return -1
		return 0

	def select(self, table, order_by=None, where=None, select=None):
		if not select:
			select = "*"

		query = "SELECT " + select + " FROM " + table
		if where:
			query += " WHERE " + where
		if order_by:
			query += " order by " + order_by

		self.cursor.execute(query)
		data = self.cursor.fetchall()
		return data

	def executeQuery(self, query):
		self.cursor.execute(query)
		data = self.cursor.fetchall()

		return data

	def count(self, table, where=None):
		query = "SELECT count(*) FROM " + table
		if where:
			query += " WHERE " + where

		self.cursor.execute(query)
		data = self.cursor.fetchall()

		return data[0][0]

	def sum(self, table, field, where=None):
		query = "SELECT sum(" + field + ") FROM " + table
		if where:
			query += " WHERE " + where

		self.cursor.execute(query)
		data = self.cursor.fetchall()
		sum = data[0][0]
		if sum is None:
			sum = 0.0

		return sum

	def max(self, table, field, where=None):
		query = "SELECT max(" + field + ") FROM " + table
		if where:
			query += " WHERE " + where

		self.cursor.execute(query)
		data = self.cursor.fetchone()

		return data[0]

	def getValue(self, id, table, field=None):
		if not field:
			field = "name"

		query = "SELECT " + field + " FROM " + table + " WHERE id=" + str(id)
		self.cursor.execute(query)
		data = self.cursor.fetchone()

		return data[0]

	def getId(self, value, table, field=None):
		if not field:
			field = "name"

		query = "SELECT id FROM " + table + " WHERE " + field +"=" + str(value)
		self.cursor.execute(query)
		data = self.cursor.fetchone()
		if data is None:
			return None
		else:
			return data[0]

	def isExist(self):
		if os.path.isfile(self.directory + self.name):
			return True
		else:
			return False

	def initDatabase(self):
		query = codecs.open(self.directoryFull + '/../../default/database.sql', 'r', 'utf8').read()
		self.cursor.executescript(query)
		self.bd.commit()


	def updateDatabase(self, version):
		if version < 1.6:
			try:
				query = "create table IF NOT EXISTS conjunta (id INTEGER primary key autoincrement, name VARCHAR(30),	month INTEGER," \
						"year INTEGER, 	money REAL );"

				self.cursor.executescript(query)
				self.bd.commit()

				query = "create table IF NOT EXISTS conjunta_tipster (conjunta INTEGER, tipster INTEGER, " \
						"constraint conjunta_tipster_conjunta_tipster_pk primary key (conjunta, tipster));"

				self.cursor.executescript(query)
				self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}".format(e))

			try:
				query = "create table IF NOT EXISTS combined (id INTEGER primary key autoincrement, bet INTEGER, date DATETIME," \
						"sport INTEGER, competition INTEGER, region INTEGER, player1 VARCHAR(150), player2 VARCHAR(150)," \
						"pick VARCHAR(150),	result VARCHAR(50));"

				self.cursor.executescript(query)
				self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}".format(e))


			try:
				query = "create table IF NOT EXISTS variable (key VARCHAR(20) primary key, 	value VARCHAR(100));"

				self.cursor.executescript(query)
				self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}".format(e))

			try:
				versionUP = self.select("variable", None, "key='version'", "value")
				if not versionUP:
					query = " INSERT INTO variable VALUES ('version', 1.6);"
					self.cursor.execute(query)
					self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}".format(e))

		if version < 1.7:
			try:
				query = "UPDATE variable SET value=1.7 WHERE key='version';"
				self.cursor.execute(query)
				self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}-".format(e))

			try:
				query = "UPDATE bet SET result=1 WHERE result='Acertada'; "
				query += "UPDATE bet SET result=0 WHERE result='Pendiente'; "
				query += "UPDATE bet SET result=2 WHERE result='Fallada'; "
				query += "UPDATE bet SET result=3 WHERE result='Nula'; "
				query += "UPDATE bet SET result=4 WHERE result='Medio Acertada'; "
				query += "UPDATE bet SET result=5 WHERE result='Medio Fallada'; "
				query += "UPDATE bet SET result=6 WHERE result='Retirada'; "
				self.cursor.executescript(query)
				self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}".format(e))

			try:
				query = "ALTER TABLE bookie ADD `country` VARCHAR(150) default 'España'"

				self.cursor.execute(query)
				self.bd.commit()
			except Exception as e:
				print("Error en BBDD: {0}".format(e))






	def close(self):
		self.cursor.close()
		self.bd.close()


	# Static

	@staticmethod
	def getYearMonth(table):
		years = {}

		bd = Bbdd()
		datos = bd.select(table, "date DESC", None, "strftime('%Y', date), strftime('%m', date)")
		bd.close()

		for i in datos:
			if i[0] in years:
				if i[1] not in years[i[0]]:
					years[i[0]].append(i[1])
			else:
				years[i[0]] = [i[1]]

		return years



