from bbdd import Bbdd
from bookie import Bookie
from constants import BetResult
from gettext import gettext as _
import gettext
from libyaml import LibYaml

class LibStats:
	coin = LibYaml().interface["coin"]

	@staticmethod
	def getYears():
		years = Bbdd.getYearMonth("bet")
		months = {"01": _("January"), "02": _("February"), "03": _("March"), "04": _("April"), "05": _("May"), "06": _("June"), "07": _("July"), "08": _("August"),
				  "09": _("September"), "10": _("October"), "11": _("November"), "12": _("December")}

		return years, months

	@staticmethod
	def getDaysOfMonth(year, month):
		days = Bbdd.getDaysOfMonth("bet", year, month)
		return days

	@staticmethod
	def getTipster(year=None, month=None):
		W, HW = BetResult.WON.value, BetResult.HALF_WON.value
		L, HL = BetResult.LOST.value, BetResult.HALF_LOST.value
		P = BetResult.PENDING.value

		if year is not None:
			sql = (
				f'SELECT tipster.name, sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.tipster=bet.tipster AND b1.sport=bet.sport AND b1.date LIKE :dp) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.tipster=bet.tipster AND b1.sport=bet.sport AND b1.date LIKE :dp) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.tipster=bet.tipster AND b1.sport=bet.sport AND b1.date LIKE :dp) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, tipster, sport'
				f' WHERE bet.tipster=tipster.id AND bet.sport=sport.id AND bet.date LIKE :dp'
				f' GROUP BY bet.tipster, bet.sport'
			)
			params = {'dp': f'{year}-{month}%'}
		else:
			sql = (
				f'SELECT tipster.name, sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.tipster=bet.tipster AND b1.sport=bet.sport) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.tipster=bet.tipster AND b1.sport=bet.sport) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.tipster=bet.tipster AND b1.sport=bet.sport) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, tipster, sport'
				f' WHERE bet.tipster=tipster.id AND bet.sport=sport.id'
				f' GROUP BY bet.tipster, bet.sport'
			)
			params = None

		bd = Bbdd()
		datasql = bd.executeQuery(sql, params)
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
			row.append("{0:.2f}".format(round((i[6]), 2)) + LibStats.coin)  # Money bet
			row.append("{0:.2f}".format(round((i[4]), 2)) + LibStats.coin)  # Profit
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[8]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getBookie(year=None, month=None):
		W, HW = BetResult.WON.value, BetResult.HALF_WON.value
		L, HL = BetResult.LOST.value, BetResult.HALF_LOST.value
		P = BetResult.PENDING.value

		if year is not None:
			sql = (
				f'SELECT bookie.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.bookie=bet.bookie AND b1.date LIKE :dp) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.bookie=bet.bookie AND b1.date LIKE :dp) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.bookie=bet.bookie AND b1.date LIKE :dp) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, bookie'
				f' WHERE bet.bookie=bookie.id AND bet.date LIKE :dp'
				f' GROUP BY bet.bookie'
			)
			params = {'dp': f'{year}-{month}%'}
		else:
			sql = (
				f'SELECT bookie.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.bookie=bet.bookie) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.bookie=bet.bookie) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.bookie=bet.bookie) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, bookie'
				f' WHERE bet.bookie=bookie.id'
				f' GROUP BY bet.bookie'
			)
			params = None

		bd = Bbdd()
		datasql = bd.executeQuery(sql, params)
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
			row.append("{0:.2f}".format(round((i[5]), 2)) + LibStats.coin)  # Money bet
			row.append("{0:.2f}".format(round((i[3]), 2)) + LibStats.coin)  # Profit
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getSport(year=None, month=None):
		W, HW = BetResult.WON.value, BetResult.HALF_WON.value
		L, HL = BetResult.LOST.value, BetResult.HALF_LOST.value
		P = BetResult.PENDING.value

		if year is not None:
			sql = (
				f'SELECT sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.sport=bet.sport AND b1.date LIKE :dp) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.sport=bet.sport AND b1.date LIKE :dp) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.sport=bet.sport AND b1.date LIKE :dp) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, sport'
				f' WHERE bet.sport=sport.id AND bet.date LIKE :dp'
				f' GROUP BY bet.sport'
			)
			params = {'dp': f'{year}-{month}%'}
		else:
			sql = (
				f'SELECT sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.sport=bet.sport) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.sport=bet.sport) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.sport=bet.sport) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, sport'
				f' WHERE bet.sport=sport.id'
				f' GROUP BY bet.sport'
			)
			params = None

		bd = Bbdd()
		datasql = bd.executeQuery(sql, params)
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
			row.append("{0:.2f}".format(round((i[5]), 2)) + LibStats.coin)  # Money bet
			row.append("{0:.2f}".format(round((i[3]), 2)) + LibStats.coin)  # Profit
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getRegion(year=None, month=None):
		W, HW = BetResult.WON.value, BetResult.HALF_WON.value
		L, HL = BetResult.LOST.value, BetResult.HALF_LOST.value
		P = BetResult.PENDING.value

		if year is not None:
			sql = (
				f'SELECT region.name, sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.region=bet.region AND b1.sport=bet.sport AND b1.date LIKE :dp) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.region=bet.region AND b1.sport=bet.sport AND b1.date LIKE :dp) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.region=bet.region AND b1.sport=bet.sport AND b1.date LIKE :dp) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, region, sport'
				f' WHERE bet.region=region.id AND bet.sport=sport.id AND bet.date LIKE :dp'
				f' GROUP BY bet.region, bet.sport'
			)
			params = {{'dp': f'{year}-{month}%'}}
		else:
			sql = (
				f'SELECT region.name, sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.region=bet.region AND b1.sport=bet.sport) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.region=bet.region AND b1.sport=bet.sport) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.region=bet.region AND b1.sport=bet.sport) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, region, sport'
				f' WHERE bet.region=region.id AND bet.sport=sport.id'
				f' GROUP BY bet.region, bet.sport'
			)
			params = None

		bd = Bbdd()
		datasql = bd.executeQuery(sql, params)
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
			row.append("{0:.2f}".format(round((i[6]), 2)) + LibStats.coin)  # Money bet
			row.append("{0:.2f}".format(round((i[4]), 2)) + LibStats.coin)  # Profit
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[8]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getMarket(year=None, month=None):
		W, HW = BetResult.WON.value, BetResult.HALF_WON.value
		L, HL = BetResult.LOST.value, BetResult.HALF_LOST.value
		P = BetResult.PENDING.value

		if year is not None:
			sql = (
				f'SELECT market.name, sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.market=bet.market AND b1.sport=bet.sport AND b1.date LIKE :dp) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.market=bet.market AND b1.sport=bet.sport AND b1.date LIKE :dp) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.market=bet.market AND b1.sport=bet.sport AND b1.date LIKE :dp) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, market, sport'
				f' WHERE bet.market=market.id AND bet.sport=sport.id AND bet.date LIKE :dp'
				f' GROUP BY bet.market, bet.sport'
			)
			params = {{'dp': f'{year}-{month}%'}}
		else:
			sql = (
				f'SELECT market.name, sport.name,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.market=bet.market AND b1.sport=bet.sport) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.market=bet.market AND b1.sport=bet.sport) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.market=bet.market AND b1.sport=bet.sport) AS prof,'
				f' count(*), SUM(bet), avg(stake), avg(quota)'
				f' FROM bet, market, sport'
				f' WHERE bet.market=market.id AND bet.sport=sport.id'
				f' GROUP BY bet.market, bet.sport'
			)
			params = None

		bd = Bbdd()
		datasql = bd.executeQuery(sql, params)
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
			row.append("{0:.2f}".format(round((i[6]), 2)) + LibStats.coin)  # Money bet
			row.append("{0:.2f}".format(round((i[4]), 2)) + LibStats.coin)  # Profit
			row.append("{0:.2f}".format(round((i[7]), 2)))  # Average Stake
			row.append("{0:.2f}".format(round((i[8]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getStake(year=None, month=None):
		W, HW = BetResult.WON.value, BetResult.HALF_WON.value
		L, HL = BetResult.LOST.value, BetResult.HALF_LOST.value
		P = BetResult.PENDING.value

		if year is not None:
			sql = (
				f'SELECT bet.stake,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.stake=bet.stake AND b1.date LIKE :dp) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.stake=bet.stake AND b1.date LIKE :dp) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.stake=bet.stake AND b1.date LIKE :dp) AS prof,'
				f' count(*), SUM(bet), avg(quota)'
				f' FROM bet WHERE bet.date LIKE :dp'
				f' GROUP BY bet.stake'
			)
			params = {{'dp': f'{year}-{month}%'}}
		else:
			sql = (
				f'SELECT bet.stake,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({W}, {HW})'
				f'  AND b1.stake=bet.stake) AS acierto,'
				f' (SELECT count(*) FROM bet AS b1 WHERE b1.result IN ({L}, {HL})'
				f'  AND b1.stake=bet.stake) AS fallo,'
				f' (SELECT SUM(profit) FROM bet AS b1 WHERE b1.result <> {P}'
				f'  AND b1.stake=bet.stake) AS prof,'
				f' count(*), SUM(bet), avg(quota)'
				f' FROM bet GROUP BY bet.stake'
			)
			params = None

		bd = Bbdd()
		datasql = bd.executeQuery(sql, params)
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
			row.append("{0:.2f}".format(round((i[5]), 2)) + LibStats.coin)  # Money bet
			row.append("{0:.2f}".format(round((i[3]), 2)) + LibStats.coin)  # Profit
			row.append("{0:.2f}".format(round((i[6]), 2)))  # Average Quota
			data.append(row)

		return data

	@staticmethod
	def getMonth(year=None, month=None, day=None):
		P = BetResult.PENDING.value
		date = str(year)
		if month is not None and month != "":
			date += "-" + str(month)
		if day is not None and day != "":
			date += "-" + day
		dp = date + "%"
		sql = (
			f'SELECT SUM(bet),'
			f' (SELECT SUM(profit) FROM bet AS b1 WHERE profit>0 AND b1.date LIKE :dp),'
			f' (SELECT SUM(profit) FROM bet AS b1 WHERE profit<0 AND b1.date LIKE :dp),'
			f' SUM(profit),'
			f' (SELECT SUM(bet) FROM bet AS b1 WHERE b1.result={P} AND b1.date LIKE :dp),'
			f' AVG(quota), count(bet),'
			f' (SELECT COUNT(*) FROM bet AS b1 WHERE profit>0 AND b1.date LIKE :dp),'
			f' (SELECT count(*) FROM bet AS b1 WHERE profit<0 AND b1.result<>{P} AND b1.date LIKE :dp),'
			f' (SELECT count(*) FROM bet AS b1 WHERE profit=0 AND b1.date LIKE :dp),'
			f' AVG(bet)'
			f' FROM bet WHERE bet.date LIKE :dp'
		)

		bd = Bbdd()
		datasql = bd.executeQuery(sql, {{'dp': dp}})
		bd.close()
		bonus = Bookie.sumBonus(f"date LIKE '{dp}'")
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
