'''
Serves as a dynamic cacheing service for Blockchain prices
'''
import sched, time, threading, statistics, urllib2

import simplejson as json

from datetime import datetime

from bs4 import BeautifulSoup

class bdata: 
	'''
	the data object to store historical bitcoin prices 
	'''
	prices = [] #{time:time, price:price}
	lock = threading.RLock

	def setPrice(self,price):
		with lock:
			self.prices.append(price)
			if len(self.prices>10):
				#We only wants the latest 10 prices 
				while len(self.prices>10):
					self.writeLog(self.prices.pop(0))

	def writeLog(self,price):
		'''
		Write the bitcoin price to log 
		'''
		with open('pricelog.json','a') as pricefile:
			pricefile.write(price)

	def getPrices(self):
		with lock:
			vol=self.getVolatility()
			if len(self.prices)>=10:
				'''
				Only calculate the price when the number of prices is greater than 10
				'''
				return (self.prices,vol)
			else:
				return (-1,-1)

	def getVolatility():
		num_price=[]
		for p in self.prices:
			num_price.append(p["price"])
		mean=statistics.mean(num_price)
		N=len(num_price)
		vol_arr=[]
		for p in num_price:
			diff=p-mean
			vol_arr.append(diff)
		vol=sum(vol_arr)*1/(N-1)

def getBitcoinPrice():
	url="https://api.coindesk.com/v1/bpi/currentprice.json"
	content=urllib2.urlopen(url).read()
	data=json.loads(content)
	price=data['bpi']['USD']['rate_float']
	raw_time=data['time']['updated']
	datetime_object = datetime.strptime(raw_time, '%b %d, %Y %H:%M:%S UTC')
	return (price, datetime_object)

def getRiskFreeRate():
	url="https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield"
	html=urllib2.urlopen(url).read()
	soup=BeautifulSoup(html)
	table = soup.find("table",{"class":"t-chart"})
	rows=table.find_all("tr")
	print rows


def calculateBS():
	'''
	Function to calculate the black scholes prices
	'''


getRiskFreeRate()