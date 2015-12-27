"""
stock trade details capture
create by royluo @ 2015.06.29
"""

import urllib2
import json
import os, sys
import db


time_key = ['09', '10', '11', '13', '14', '15']

time_map = {'09':['35', '40', '45', '50', '55'],
				'10':['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
				'11':['00', '05', '10', '15', '20', '25', '30'],
				
				'13':['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
				'14':['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'],
				'15':['00']
				}
				
def time2Sec(time_str):
	x = time_str.split(':')
	hour = int(x[0])
	mint = int(x[1])
	sec = int(x[2])
	return hour * 60 * 60 + mint * 60 + sec

def timeSlot2Sec(h_str, m_str):
	h = int(h_str)
	m = int(m_str)
	return h * 60 * 60 + m * 60

def isTimeOk(time_str, h_str, m_str):
	x = time2Sec(time_str)
	y_up = timeSlot2Sec(h_str, m_str);
	y_down = y_up - 300
	if x >= y_down and x <= y_up:
		return True
	else:
		return False
	

def print_msg(info_string):
	print "[INFO] " + info_string 

def err_msg(err_string):
	print "[ERR] " + err_string

def tradeDetailsGet(site):
	html = urllib2.urlopen(site).read()

	stock_trade = json.loads(html)
	#print_msg('begin: ' + stock_trade['begin'] + ',' + 'end: ' + stock_trade['end'])
	sys.stdout.write(".")
	return stock_trade['zhubi_list']
	

def tradeSiteByCode(stock_code, hour, min):
	site = "http://quotes.money.163.com/service/zhubi_ajax.html?symbol="+stock_code + "&end=" + hour + "%3A" + min + "%3A00"
	#print site
	return site


def dbItemInsert(zhubi_list, db_conn, db_table_name, h, m):
	for zhubi in zhubi_list:
		if isTimeOk(zhubi['DATE_STR'], h, m):
			#print "DATE_STR: %s  PRICE: %s VOLUME_INC: %s " % (zhubi["DATE_STR"], zhubi["PRICE"], zhubi["VOLUME_INC"])
			insert_table_cmd = "INSERT INTO " + db_table_name + " (TIME, PRICE, VOLUME_INC) VALUES (" +"\"" + zhubi["DATE_STR"] + "\"" + "," + str(zhubi["PRICE"]) +"," + str(zhubi["VOLUME_INC"]) + ")"
			#print insert_table_cmd
			db.dbInsertTable(db_conn, insert_table_cmd)
		else:
			continue;
	db.dbCommit(db_conn)


def tradeItemStore(stock_code, db_connect, db_table_name):
	print_msg("start load data...")
	for k in time_key:
		for v in time_map[k]:
			site = tradeSiteByCode(stock_code, k, v)
			zhubi_list = tradeDetailsGet(site)
			dbItemInsert(zhubi_list, db_connect, db_table_name, k, v)
	print_msg("\nload data ok!")
	return

stock_code = "000751"
stock_db = 'stockdata.db'
db_table_name = "tb_" + stock_code


def tradeDataStore():
	table_name = db_table_name
	db_conn = db.dbConnect(stock_db)
	table_create_cmd = "CREATE TABLE " + table_name + " (TIME CHARACTER(20), PRICE FLOAT, VOLUME_INC INT, TRADE_TYPE INT);"
	db.dbCreateTable(db_conn, table_name, table_create_cmd)
	tradeItemStore(stock_code, db_conn, table_name)
	db.dbClose(db_conn)
	return




def tradeInfoQuery():
	db_name = stock_db
	db_conn = db.dbConnect(stock_db)
	cursor = db_conn.cursor()

	cursor.execute("SELECT TIME, PRICE, VOLUME_INC from " + db_table_name)
	results = cursor.fetchall()
	db.dbClose(db_conn)
	for row in results:
		print "time: %s, price %f, volume %s" %(row[0], row[1], row[2])

tradeDataStore()
#tradeInfoQuery()
