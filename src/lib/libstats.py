import sys, os
from bbdd import Bbdd

class LibStats:
	@staticmethod
	def getYears():
		years = Bbdd.getYearMonth("bet")
		months = {"01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril", "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
		          "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"}
		return years, months

	@staticmethod
	def getTipster(year=None, month=None):
		if year is not None:
			date = str(year)+"-"+str(month)
			sql = 'select tipster.name, sport.name, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada") ' \
			      'and b1.tipster = bet.tipster and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as acierto, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and b1.tipster = bet.tipster ' \
			      'and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(REPLACE(profit,",",".")) ' \
			      'from bet as b1 WHERE b1.result <> "Pendiente" and b1.tipster = bet.tipster and b1.sport=bet.sport) as prof, count(*), ' \
			      'SUM(REPLACE(bet,",",".")), avg(stake), avg(quota) from bet, tipster, sport WHERE bet.tipster=tipster.id ' \
			      'and bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.tipster,bet.sport '

		else:
			sql = 'SELECT tipster.name, sport.name, (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ' \
			      '("Acertada", "Medio Acertada") AND b1.tipster = bet.tipster AND b1.sport=bet.sport) AS acierto, ' \
			      '(SELECT count(*) FROM bet AS b1 WHERE b1.result IN ("Fallada", "Medio Fallada") AND ' \
			      'b1.tipster = bet.tipster AND b1.sport=bet.sport) AS fallo, (SELECT SUM(REPLACE(profit,",",".")) ' \
			      'FROM bet AS b1 WHERE b1.result <> "Pendiente" AND b1.tipster = bet.tipster AND b1.sport = bet.sport) AS prof, count(*), ' \
			      'SUM(REPLACE(bet,",",".")), avg(stake), avg(quota) FROM bet, tipster, sport ' \
			      'WHERE bet.tipster=tipster.id AND bet.sport=sport.id GROUP BY bet.tipster,bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			row = []
			row.append(i[0])  # Tipster
			row.append(i[1])  # Sports
			row.append(str(i[5]))  # Number of bets
			try:
				win = i[2]/(i[2]+i[3])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			row.append(str(win)+"%")
			row.append(str(i[6]))  # Money bet
			row.append(str(i[4]))  # Profit
			row.append(str(i[7]))  # Average Stake
			row.append(str(i[8]))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getBookie(year=None, month=None):
		if year is not None:
			date = str(year) + "-" + str(month)
			sql = 'select bookie.name, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
			      '("Acertada", "Medio Acertada") and b1.bookie = bet.bookie and b1.date LIKE "' + date + '%") as acierto, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
			      'b1.bookie = bet.bookie and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(REPLACE(profit,",",".")) ' \
			      'from bet as b1 WHERE b1.result <> "Pendiente" and b1.bookie = bet.bookie and b1.date LIKE "' + date + '%") as prof, count(*), ' \
			      'SUM(REPLACE(bet,",",".")), avg(stake), avg(quota) from bet, bookie ' \
			      'WHERE bet.bookie=bookie.id and bet.date LIKE "' + date + '%" GROUP BY bet.bookie'
		else:
			sql = 'select bookie.name, (SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada")' \
			      ' and b1.bookie = bet.bookie) as acierto, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
			      '("Fallada", "Medio Fallada") and b1.bookie = bet.bookie) as fallo, ' \
			      '(SELECT SUM(REPLACE(profit,",",".")) from bet as b1 WHERE b1.result <> "Pendiente" and' \
			      ' b1.bookie = bet.bookie) as prof, count(*), SUM(REPLACE(bet,",",".")), avg(stake), ' \
			      'avg(quota) from bet, bookie WHERE bet.bookie=bookie.id GROUP BY bet.bookie'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			row = []
			row.append(i[0])  # Name
			row.append(str(i[4]))  # Number of bets
			try:
				win = i[1] / (i[1] + i[2])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			win = round(win, 2)
			row.append(str(win) + "%")
			row.append(str(i[5]))  # Money bet
			row.append(str(i[3]))  # Profit
			row.append(str(i[6]))  # Average Stake
			row.append(str(i[7]))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getSport(year=None, month=None):
		if year is not None:
			date = str(year) + "-" + str(month)
			sql = 'select sport.name, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
			      '("Acertada", "Medio Acertada") and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as acierto, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
			      'b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(REPLACE(profit,",",".")) ' \
			      'from bet as b1 WHERE b1.result <> "Pendiente" and b1.sport=bet.sport) as prof, count(*), ' \
			      'SUM(REPLACE(bet,",",".")), avg(stake), avg(quota) from bet, sport ' \
			      'WHERE bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.sport'
		else:
			sql = 'select sport.name, (SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada")' \
			      ' and b1.sport = bet.sport) as acierto, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
			      '("Fallada", "Medio Fallada") and b1.sport = bet.sport) as fallo, ' \
			      '(SELECT SUM(REPLACE(profit,",",".")) from bet as b1 WHERE b1.result <> "Pendiente" and' \
			      ' b1.sport = bet.sport) as prof, count(*), SUM(REPLACE(bet,",",".")), avg(stake), ' \
			      'avg(quota) from bet, sport WHERE bet.sport=sport.id GROUP BY bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			row = []
			row.append(i[0])  # Name
			row.append(str(i[4]))  # Number of bets
			try:
				win = i[1] / (i[1] + i[2])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			win = round(win, 2)
			row.append(str(win) + "%")
			row.append(str(i[5]))  # Money bet
			row.append(str(i[3]))  # Profit
			row.append(str(i[6]))  # Average Stake
			row.append(str(i[7]))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getRegion(year=None, month=None):
		if year is not None:
			date = str(year)+"-"+str(month)
			sql = 'select region.name, sport.name, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada") ' \
			      'and b1.region = bet.region and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as acierto, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and b1.region = bet.region ' \
			      'and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(REPLACE(profit,",",".")) ' \
			      'from bet as b1 WHERE b1.result <> "Pendiente" and b1.region = bet.region and b1.sport=bet.sport) as prof, count(*), ' \
			      'SUM(REPLACE(bet,",",".")), avg(stake), avg(quota) from bet, region, sport WHERE bet.region=region.id ' \
			      'and bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.region,bet.sport '

		else:
			sql = 'SELECT region.name, sport.name, (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ' \
			      '("Acertada", "Medio Acertada") AND b1.region = bet.region AND b1.sport=bet.sport) AS acierto, ' \
			      '(SELECT count(*) FROM bet AS b1 WHERE b1.result IN ("Fallada", "Medio Fallada") AND ' \
			      'b1.region = bet.region AND b1.sport=bet.sport) AS fallo, (SELECT SUM(REPLACE(profit,",",".")) ' \
			      'FROM bet AS b1 WHERE b1.result <> "Pendiente" AND b1.region = bet.region AND b1.sport = bet.sport) AS prof, count(*), ' \
			      'SUM(REPLACE(bet,",",".")), avg(stake), avg(quota) FROM bet, region, sport ' \
			      'WHERE bet.region=region.id AND bet.sport=sport.id GROUP BY bet.region, bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			row = []
			row.append(i[0])  # Region
			row.append(i[1])  # Sports
			row.append(str(i[5]))  # Number of bets
			try:
				win = i[2] / (i[2] + i[3])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			row.append(str(win) + "%")
			row.append(str(i[6]))  # Money bet
			row.append(str(i[4]))  # Profit
			row.append(str(i[7]))  # Average Stake
			row.append(str(i[8]))  # Average Quota
			data.append(row)

		return data

