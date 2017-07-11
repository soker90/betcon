import sys, sqlite3, os
from os.path import expanduser


class Bbdd:
	directory = expanduser("~") + "/.betcon/"
	name = "betcon.sqlite3"

	def __init__(self):
		exist = False
		if self.isExist():
			exist = True
		self.bd = sqlite3.connect(self.directory + self.name)
		self.cursor = self.bd.cursor()

		if not exist:
			self.initDatabase()


	def insert(self, columns, values, table):
		aux = ', '.join('?' * len(values))
		if len(columns) == 1:
			columns = '('+str(columns[0])+')'
		else:
			columns = str(tuple(columns))
		query = "INSERT INTO " + table + columns + " VALUES(%s);" % aux

		self.cursor.execute(query, values)
		self.bd.commit()

	def select(self, table, order_by=None, where=None):
		query = "SELECT * FROM " + table
		if where:
			query += " WHERE " + where
		if order_by:
			query += " order by " + order_by

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

	def getValue(self, id, table, field=None):
		if not field:
			field = "name"

		query = "SELECT " + field + " FROM " + table + " WHERE id=" + str(id)

		self.cursor.execute(query)
		data = self.cursor.fetchone()

		return data[0]

	def isExist(self):
		if os.path.isfile(self.directory + self.name):
			return True
		else:
			return False

	def initDatabase(self):
		query = open('../default/database.sql', 'r').read()
		self.cursor.execute(query)
		self.bd.commit()


	def close(self):
		self.cursor.close()
		self.bd.close()

