from bbdd import Bbdd
from bookie import Bookie
from gettext import gettext as _
import gettext

class LibStats:
	@staticmethod
	def getYears():
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../../lang/mo")
		years = Bbdd.getYearMonth("bet")
		months = {"01": _("January"), "02": _("February"), "03": _("March"), "04": _("April"), "05": _("May"), "06": _("June"), "07": _("July"), "08": _("August"),
				  "09": _("September"), "10": _("October"), "11": _("November"), "12": _("December")}

		return years, months

	@staticmethod
	def getTipster(year=None, month=None):
		if year is not None:
			date = str(year)+"-"+str(month)
			sql = 'select tipster.name, sport.name, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada") ' \
				  'and b1.tipster = bet.tipster and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as acierto, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and b1.tipster = bet.tipster ' \
				  'and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(profit) ' \
				  'from bet as b1 WHERE b1.result <> "Pendiente" and b1.tipster = bet.tipster and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) from bet, tipster, sport WHERE bet.tipster=tipster.id ' \
				  'and bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.tipster,bet.sport '

		else:
			sql = 'SELECT tipster.name, sport.name, (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ' \
				  '("Acertada", "Medio Acertada") AND b1.tipster = bet.tipster AND b1.sport=bet.sport) AS acierto, ' \
				  '(SELECT count(*) FROM bet AS b1 WHERE b1.result IN ("Fallada", "Medio Fallada") AND ' \
				  'b1.tipster = bet.tipster AND b1.sport=bet.sport) AS fallo, (SELECT SUM(profit) ' \
				  'FROM bet AS b1 WHERE b1.result <> "Pendiente" AND b1.tipster = bet.tipster AND b1.sport = bet.sport) AS prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) FROM bet, tipster, sport ' \
				  'WHERE bet.tipster=tipster.id AND bet.sport=sport.id GROUP BY bet.tipster,bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			row = []
			if i[4] is None:
				continue
			row.append(i[0])  # Tipster
			row.append(i[1])  # Sports
			row.append(str(i[5]))  # Number of bets
			try:
				win = i[2]/(i[2]+i[3])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			row.append("{0:.2f}%".format(round((win), 2)))
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Money bet
			row.append("{0:.2f}".format(round((i[4]), 2)))  # Profit
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[8]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getBookie(year=None, month=None):
		if year is not None:
			date = str(year) + "-" + str(month)
			sql = 'select bookie.name, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
				  '("Acertada", "Medio Acertada") and b1.bookie = bet.bookie and b1.date LIKE "' + date + '%") as acierto, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
				  'b1.bookie = bet.bookie and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(profit) ' \
				  'from bet as b1 WHERE b1.result <> "Pendiente" and b1.bookie = bet.bookie and b1.date LIKE "' + date + '%") as prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) from bet, bookie ' \
				  'WHERE bet.bookie=bookie.id and bet.date LIKE "' + date + '%" GROUP BY bet.bookie'
		else:
			sql = 'select bookie.name, (SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada")' \
				  ' and b1.bookie = bet.bookie) as acierto, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
				  '("Fallada", "Medio Fallada") and b1.bookie = bet.bookie) as fallo, ' \
				  '(SELECT SUM(profit) from bet as b1 WHERE b1.result <> "Pendiente" and' \
				  ' b1.bookie = bet.bookie) as prof, count(*), SUM(bet), avg(stake), ' \
				  'avg(quota) from bet, bookie WHERE bet.bookie=bookie.id GROUP BY bet.bookie'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			if i[3] is None:
				continue
			row = []
			row.append(i[0])  # Name
			row.append(str(i[4]))  # Number of bets
			try:
				win = i[1] / (i[1] + i[2])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			win = round(win, 2)
			row.append("{0:.2f}%".format(round((win), 2)))
			row.append("{0:.2f}".format(round((i[5]), 2)))  # Money bet
			row.append("{0:.2f}".format(round((i[3]), 2)))  # Profit
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getSport(year=None, month=None):
		if year is not None:
			date = str(year) + "-" + str(month)
			sql = 'select sport.name, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
				  '("Acertada", "Medio Acertada") and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as acierto, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
				  'b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(profit) ' \
				  'from bet as b1 WHERE b1.result <> "Pendiente" and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) from bet, sport ' \
				  'WHERE bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.sport'
		else:
			sql = 'select sport.name, (SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada")' \
				  ' and b1.sport = bet.sport) as acierto, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
				  '("Fallada", "Medio Fallada") and b1.sport = bet.sport) as fallo, ' \
				  '(SELECT SUM(profit) from bet as b1 WHERE b1.result <> "Pendiente" and' \
				  ' b1.sport = bet.sport) as prof, count(*), SUM(bet), avg(stake), ' \
				  'avg(quota) from bet, sport WHERE bet.sport=sport.id GROUP BY bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			if i[3] is None:
				continue
			row = []
			row.append(i[0])  # Name
			row.append(str(i[4]))  # Number of bets
			try:
				win = i[1] / (i[1] + i[2])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			win = round(win, 2)
			row.append("{0:.2f}%".format(round(win, 2)))
			row.append("{0:.2f}".format(round((i[5]), 2)))  # Money bet
			row.append("{0:.2f}".format(round((i[3]), 2)))  # Profit
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Quota
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
				  'and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(profit) ' \
				  'from bet as b1 WHERE b1.result <> "Pendiente" and b1.region = bet.region and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) from bet, region, sport WHERE bet.region=region.id ' \
				  'and bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.region,bet.sport '

		else:
			sql = 'SELECT region.name, sport.name, (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ' \
				  '("Acertada", "Medio Acertada") AND b1.region = bet.region AND b1.sport=bet.sport) AS acierto, ' \
				  '(SELECT count(*) FROM bet AS b1 WHERE b1.result IN ("Fallada", "Medio Fallada") AND ' \
				  'b1.region = bet.region AND b1.sport=bet.sport) AS fallo, (SELECT SUM(profit) ' \
				  'FROM bet AS b1 WHERE b1.result <> "Pendiente" AND b1.region = bet.region AND b1.sport = bet.sport) AS prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) FROM bet, region, sport ' \
				  'WHERE bet.region=region.id AND bet.sport=sport.id GROUP BY bet.region, bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			if i[4] is None:
				continue
			row = []
			row.append(i[0])  # Region
			row.append(i[1])  # Sports
			row.append(str(i[5]))  # Number of bets
			try:
				win = i[2] / (i[2] + i[3])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			row.append("{0:.2f}%".format(round(win, 2)))
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Money bet
			row.append("{0:.2f}".format(round((i[4]), 2)))  # Profit
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[8]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getMarket(year=None, month=None):
		if year is not None:
			date = str(year)+"-"+str(month)
			sql = 'select market.name, sport.name, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada") ' \
				  'and b1.market = bet.market and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as acierto, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and b1.market = bet.market ' \
				  'and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(profit) ' \
				  'from bet as b1 WHERE b1.result <> "Pendiente" and b1.market = bet.market and b1.sport=bet.sport and b1.date LIKE "' + date + '%") as prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) from bet, market, sport WHERE bet.market=market.id ' \
				  'and bet.sport=sport.id and bet.date LIKE "' + date + '%" GROUP BY bet.market, bet.sport '

		else:
			sql = 'SELECT market.name, sport.name, (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ' \
				  '("Acertada", "Medio Acertada") AND b1.market = bet.market AND b1.sport=bet.sport) AS acierto, ' \
				  '(SELECT count(*) FROM bet AS b1 WHERE b1.result IN ("Fallada", "Medio Fallada") AND ' \
				  'b1.market = bet.market AND b1.sport=bet.sport) AS fallo, (SELECT SUM(profit) ' \
				  'FROM bet AS b1 WHERE b1.result <> "Pendiente" AND b1.market = bet.market AND b1.sport = bet.sport) AS prof, count(*), ' \
				  'SUM(bet), avg(stake), avg(quota) FROM bet, market, sport ' \
				  'WHERE bet.market=market.id AND bet.sport=sport.id GROUP BY bet.market, bet.sport'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			if i[4] is None:
				continue
			row = []
			row.append(i[0])  # Region
			row.append(i[1])  # Sports
			row.append(str(i[5]))  # Number of bets
			try:
				win = i[2] / (i[2] + i[3])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			row.append("{0:.2f}%".format(round(win, 2)))
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Money bet
			row.append("{0:.2f}".format(round((i[4]), 2)))  # Profit
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[8]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getStake(year=None, month=None):
		if year is not None:
			date = str(year) + "-" + str(month)
			sql = 'select bet.stake, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
				  '("Acertada", "Medio Acertada") and b1.stake=bet.stake and b1.date LIKE "' + date + '%") as acierto, ' \
				  '(SELECT count(*) from bet as b1 WHERE b1.result in ("Fallada", "Medio Fallada") and ' \
				  'b1.stake=bet.stake and b1.date LIKE "' + date + '%") as fallo, (SELECT SUM(profit) ' \
				  'from bet as b1 WHERE b1.result <> "Pendiente" and b1.stake=bet.stake and b1.date LIKE "' + date + '%") as prof, count(*), ' \
				  'SUM(bet), avg(quota) from bet WHERE bet.date LIKE "' + date + '%" GROUP BY bet.stake'
		else:
			sql = 'select bet.stake, (SELECT count(*) from bet as b1 WHERE b1.result in ("Acertada", "Medio Acertada")' \
				  ' and b1.stake = bet.stake) as acierto, (SELECT count(*) from bet as b1 WHERE b1.result in ' \
				  '("Fallada", "Medio Fallada") and b1.stake = bet.stake) as fallo, ' \
				  '(SELECT SUM(profit) from bet as b1 WHERE b1.result <> "Pendiente" and' \
				  ' b1.stake = bet.stake) as prof, count(*), SUM(bet), ' \
				  'avg(quota) from bet GROUP BY bet.stake'

		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()

		data = []
		for i in datasql:
			if i[3] is None:
				continue
			row = []
			row.append(str(i[0]))  # Stake
			row.append(str(i[4]))  # Number of bets
			try:
				win = i[1] / (i[1] + i[2])  # Percentage of win bet
			except ZeroDivisionError:
				win = 0
			win = win * 100
			row.append("{0:.2f}%".format(round(win, 2)))
			row.append("{0:.2f}".format(round((i[5]), 2)))  # Money bet
			row.append("{0:.2f}".format(round((i[3]), 2)))  # Profit
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getMonth(year=None, month=None):
		date = str(year) + "-" + str(month)
		sql = 'select SUM(bet), ' \
			  '(select SUM(profit) from bet as b1 WHERE profit>0 AND b1.date LIKE "' + date + '%"), ' \
			  '(select SUM(profit) from bet as b1 WHERE profit<0 AND b1.date LIKE "' + date + '%"), ' \
			  'SUM(profit), (select SUM(bet) from bet as b1 WHERE b1.result="Pendiente" AND bet.date LIKE "' + date + '%"), ' \
			  'AVG(quota), count(bet), (select COUNT(*) from bet as b1 WHERE profit>0 AND b1.date LIKE "' + date + '%"), ' \
			  '(select count(*) from bet as b1 WHERE profit<0 AND b1.result<>"Pendiente" AND b1.date LIKE "' + date + '%"),' \
			  '(select count(*) from bet as b1 WHERE profit=0 AND b1.date LIKE "' + date + '%"), AVG(bet)' \
			  ' from bet WHERE bet.date LIKE "' + date + '%"'


		bd = Bbdd()
		datasql = bd.executeQuery(sql)
		bd.close()
		bonus = Bookie.sumBonus("date LIKE '" + date + "%'")
		datasql = datasql[0]
		if bonus is None:
			bonus = 0

		if datasql[0] == 0:
			return [0, 0, 0, 0, 0, "0%", 0, 0, 0, 0, 0, "0%", 0]

		yi = "{0:.2f}%".format(round(((datasql[3]+bonus)/datasql[0])*100, 2))
		quota = float("{0:.2f}".format(datasql[5], 2))
		bet = float("{0:.2f}".format(datasql[10], 2))

		aciertos = "{0:.2f}%".format(round((datasql[7] / datasql[6]) * 100, 2))
		data0 = "{0:.2f}".format(round(datasql[0], 2))
		data1 = 0.0 if datasql[1] is None else "{0:.2f}".format(round(datasql[1] + bonus, 2))
		data2 = 0.0 if datasql[2] is None else "{0:.2f}".format(round(datasql[2], 2))
		data3 = 0.0 if datasql[3] is None else "{0:.2f}".format(round(datasql[3] + bonus, 2))
		data4 = 0.0 if datasql[4] is None else "{0:.2f}".format(round(datasql[4], 2))
		data = [data0, data1, data2, data3, data4, yi, quota, datasql[6], datasql[7],
				datasql[8], datasql[9], aciertos, bet]

		return data
