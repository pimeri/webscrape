import urllib2
import re
import sys
import time
import datetime

start_time = time.time()
date = sys.argv[-1]
tickers = sys.argv[1:-1]
failed_tickers = []
urlTemplate = "https://finance.yahoo.com/quote/TICKER/PAGE?p=TICKER"
failed_tickers = []


try:
	dt = datetime.datetime.strptime(date, '%m-%d-%Y')
	endTime = int((time.mktime(dt.timetuple()) - 3600))
	startTime = endTime - 86400
except:
	print 'Error: invalid date format, must be mm-dd-yyyy'
	exit()

for ticker in tickers:
	try:
		url = urlTemplate.replace("TICKER",ticker).replace("PAGE","profile")
		page = urllib2.urlopen(url).read()
		m1 = re.search( 'profile for (.*?) \(', page)
		m2 = re.search('founded in (.*) and .* in ([a-zA-z\s]*, [a-zA-z]*)',page)
		m3 = re.search('\"fullTimeEmployees\":([0-9]*)', page)

		if (m1 == None or m2 == None or m3 == None):
			raise Exception('failed ticker')
		print 'name\t\t: ', m1.group(1)
		print 'founded\t\t: ' , m2.group(1)
		print 'employees\t:' ,  m3.group(1)
		print 'Headquarters\t: ', m2.group(2)
		print 'Prev close:\t:', " void"
		print 'open price:\t:', " void \n"
	except:
		failed_tickers.append(ticker)
	# historyUrl = "https://finance.yahoo.com/quote/TICKER/history?period1=1551081600&period2=1551254400&interval=1d&filter=history&frequency=1d"

print 'failed tickers: ', failed_tickers
print("--- %s seconds ---" % (time.time() - start_time))
