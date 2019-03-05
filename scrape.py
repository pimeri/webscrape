import urllib2
import re
import sys
import time
import datetime
# import re

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


# exit()


for ticker in tickers:
	try:
		url_start = time.time()
		url = urlTemplate.replace("TICKER",ticker).replace("PAGE","profile")
		# print ("--- %s seconds for the request --- " % (time.time() - url_start))
		temp_page = urllib2.urlopen(url)
		print ("--- %s seconds for the request --- " % (time.time() - url_start))
		read_start = time.time()
		page = temp_page.read()
		print ("--- %s seconds for the request --- " % (time.time() - read_start))
		# page = urllib2.urlopen(url).read()
		# profile page
		m1 = re.search( 'profile for (.*?) \(', page)
		m  = re.search('founded in (.*) and .* in ([a-zA-z\s]*, [a-zA-z]*)',page)
		m2 = re.search('\"fullTimeEmployees\":([0-9]*)', page)

		if (m1 == None or m == None or m2 == None):
			raise Exception('failed ticker')
		print 'name\t\t: ', m1.group(1)
		print 'founded\t\t: ' , m.group(1)
		print 'employees\t:' ,  m2.group(1)
		print 'Headquarters\t: ', m.group(2)
		print 'Prev close:\t:', " void"
		print 'open price:\t:', " void \n"
	except:
		failed_tickers.append(ticker)
	# historyUrl = "https://finance.yahoo.com/quote/TICKER/history?period1=1551081600&period2=1551254400&interval=1d&filter=history&frequency=1d"

print 'failed tickers: ', failed_tickers
print("--- %s seconds ---" % (time.time() - start_time))
