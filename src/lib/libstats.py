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
			sql = 'select tipster.name, sport.name, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
			      '("Acertada", "Medio Acertada") and b1.tipster = bet.tipster and b1.sport=bet.sport and b1.date LIKE "' + date \
			      + '%") as acierto, (SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
			      'b1.tipster = bet.tipster and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, sum(profit), count(*), sum(bet), ' \
			      'avg(stake), avg(quota) from bet, tipster, sport WHERE bet.tipster=tipster.id and bet.sport=sport.id and bet.date LIKE "' + date + '%" '\
			      'GROUP BY bet.tipster,bet.sport'
		else:
			sql = 'select tipster.name, sport.name, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
			      '("Acertada", "Medio Acertada") and b1.tipster = bet.tipster and b1.sport=bet.sport) as acierto, ' \
			      '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
			      'b1.tipster = bet.tipster and b1.sport=bet.sport) as fallo, sum(profit), count(*), sum(bet), ' \
			      'avg(stake), avg(quota) from bet, tipster, sport WHERE bet.tipster=tipster.id and bet.sport=sport.id ' \
			      'GROUP BY bet.tipster,bet.sport'

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

