import requests
import re
import sys
import time
import datetime

start_time 		= time.time()
date 			= sys.argv[-1]
tickers 		= sys.argv[1:-1]
failed_tickers 	= []
session			= requests.Session()
urlTemplate 	= "https://finance.yahoo.com/quote/TICKER?p=TICKER"
urlTemplate2 	= "https://finance.yahoo.com/quote/TICKER/history?period1=TIME1&period2=TIME2&interval=1d&filter=history&frequency=1d"

try:
	dt = datetime.datetime.strptime(date, '%m-%d-%Y')
	endTime = int((time.mktime(dt.timetuple()) - 3600))
	startTime = endTime - 604800
except:
	print 'Error: invalid date format, must be mm-dd-yyyy'
	exit()

for ticker in tickers:
	try:
		url = urlTemplate.replace("TICKER",ticker).replace("PAGE","profile")
		page = session.get(url).text

		m1 = re.search( 'Summary for (.*?) -', page)
		m2 = re.search('founded in (.*?) and .*? in ([a-zA-z\s]*, [a-zA-z]*)',page)
		m3 = re.search('\"fullTimeEmployees\":([0-9]*)', page)
		m5 = re.search( ticker + '":{.*"marketCap":{"raw":([0-9]*)', page)

		url = urlTemplate2.replace("TICKER",ticker).replace("TIME1",str(startTime)).replace("TIME2",str(endTime))
		page = session.get(url).text
		m4 = re.search('"prices":.*"open":([0-9.]*).*"close":([0-9.]*)',page)

		if (m1 == None or m2 == None or m3 == None or m4 == None ):
			raise Exception('failed ticker')
		
		print 'name\t\t: '		, m1.group(1)
		print 'founded\t\t: ' 	, m2.group(1)
		print 'employees\t: ' 	, m3.group(1)
		print 'City\t\t: '		, m2.group(2).split(", ")[0]
		print 'State\t\t: '		, m2.group(2).split(", ")[1]
		print 'Prev close\t: '	, m4.group(1)
		print 'open price\t: '	, m4.group(2)
		print 'marketCap\t: ' 	, m5.group(1), "\n"
	except:
		failed_tickers.append(ticker)
		
if failed_tickers:
	print 'failed tickers: ', failed_tickers
print("--- Finished in %s seconds ---" % (time.time() - start_time))

	
