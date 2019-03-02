import urllib2
from bs4 import BeautifulSoup
from time import sleep
import re

ticker = 'MSFT'

urlTemplate = "https://finance.yahoo.com/quote/TICKER/PAGE?p=TICKER"

url = urlTemplate.replace("TICKER",ticker).replace("PAGE","profile")


page = urllib2.urlopen(url).read()


historyUrl = "https://finance.yahoo.com/quote/TICKER/history?period1=1551081600&period2=1551254400&interval=1d&filter=history&frequency=1d"

# print page.read()
# data-reactid="80">([0-9]*.[0-9]*B)

# profile page
m1 = re.search( 'profile for (.*?) \(', page)
m  = re.search('founded in (.*) and .*quartered in ([a-zA-z]*, [a-zA-z]*)',page)

# 
url = urlTemplate.replace("TICKER",ticker).replace("/PAGE","")
print url
# m2 = re.search( 'data-reactid="80">([0-9]*.[0-9]*B)', page)

# print m.group(1)

# print url

print 'name\t\t: ', m1.group(1)
print 'founded\t\t: ' , m.group(1)
print 'employees\t:' ,  " void"
print 'Headquarters\t: ', m.group(2)
print 'Prev close:\t:', " void"
print 'open price:\t:', " void"
# print 'Market cap:\t:', m2

