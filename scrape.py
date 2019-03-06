import requests
import re
import sys
import time
import datetime
import tableController


start_time 		= time.time()
date 			= sys.argv[-1]
tickers 		= sys.argv[1:-1]
failed_tickers 	= []
# this session object allows me to reuse one TCP connection which makes a significant difference in speed
session			= requests.Session()
urlTemplate 	= "https://finance.yahoo.com/quote/{TICKER}?p={TICKER}"
urlTemplate2 	= "https://finance.yahoo.com/quote/{TICKER}/history?period1={PERIOD1}&period2={PERIOD2}&interval=1d&filter=history&frequency=1d"

# here I attempt to convert the user input date to unix time
#  note I leave it in PST(the dafult) as it works better with hte NYSE stock exchange open time

try:
	dt = datetime.datetime.strptime(date, '%m-%d-%Y')
	endTime = int((time.mktime(dt.timetuple()) - 3600))
	startTime = endTime - 604800
except:
	print 'Error: invalid date format, must be mm-dd-yyyy'
	exit()

tableController.initTable()
for ticker in tickers:
	try:
		url = urlTemplate.format(TICKER=ticker)
		page = session.get(url).text

		# regular expressions to capture the data I need
		m1 = re.search( 'Summary for (.*?) -', page)
		m2 = re.search('founded in (.*?) and .*? in ([a-zA-z\s]*, [a-zA-z]*)', page)
		m3 = re.search('\"fullTimeEmployees\":([0-9]*)', page)
		m5 = re.search( ticker + '":{.*"marketCap":{"raw":([0-9]*)', page)

		url = urlTemplate2.format(TICKER=ticker,PERIOD1=startTime,PERIOD2=endTime)
		page = session.get(url).text
		m4 = re.search('"prices":.*"open":([0-9.]*).*"close":([0-9.]*)',page)

		if (m1 == None or m2 == None or m3 == None or m4 == None or m5 == None):
			raise Exception('failed ticker')
		# here I pack all the capture groups from the regexes into a tuple and send it to the
		# sql controller 
		statement = (
				m1.group(1),
				m2.group(1),
				m3.group(1),
				m2.group(2).split(", ")[0],
				m2.group(2).split(", ")[1],
				m4.group(1),
				m4.group(2),
				m5.group(1),
				date
			)
		tableController.insert(statement)
	except:
		failed_tickers.append(ticker)
		
if failed_tickers:
	print 'failed tickers: ', failed_tickers

tableController.printTable()
print("--- Finished in %s seconds ---" % (time.time() - start_time))

