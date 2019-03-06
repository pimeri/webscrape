import sqlite3
import pandas

pandas.set_option('display.max_colwidth',1000)

def initTable():
	conn = sqlite3.connect('stocks.db')
	cursor = conn.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS stocks 
             (id INTEGER primary key, 
             company text, 
             founded int,
             employees int,
             city text,
             state text,
             prevclose real,
             openprice real,
             marketcap real,
             date      text)

          ''')
	conn.commit()
	conn.close()

def insert(data):
	conn = sqlite3.connect('stocks.db')
	cursor = conn.cursor()
	cursor.execute("INSERT INTO stocks VALUES (null,?,?,?,?,?,?,?,?,?)", data)
	conn.commit()
	conn.close()

def printTable():
	conn = sqlite3.connect('stocks.db')
	print pandas.read_sql_query("SELECT * FROM stocks", conn)
	conn.close()


def printByCompany(companyName):
	conn = sqlite3.connect('stocks.db')
	cursor = conn.cursor()
	t = (companyName,)
	print pandas.read_sql_query("SELECT * FROM 'stocks' WHERE company = ? ",conn,params=t)
	

def printByDate(date):
	conn = sqlite3.connect('stocks.db')
	cursor = conn.cursor()
	date += "-9:30AM"
	t = (date,)
	print pandas.read_sql_query("SELECT * FROM 'stocks' WHERE date = ? ",conn,params=t)

def printByState(state):
	conn = sqlite3.connect('stocks.db')
	cursor = conn.cursor()
	t = (state,)
	print pandas.read_sql_query("SELECT * FROM 'stocks' WHERE state = ? ",conn,params=t)

def printByOpen(price):
	conn = sqlite3.connect('stocks.db')
	cursor = conn.cursor()
	t = (price,)
	print pandas.read_sql_query("SELECT * FROM 'stocks' WHERE openprice >= ? ",conn,params=t)
