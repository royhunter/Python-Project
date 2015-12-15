"""
stock trade details capture
create by royluo @ 2015.06.29
"""

import urllib2
import json
import sqlite3
import os

time_key = ['09', '10', '11', '13', '14']

time_map = {'09':['35', '40', '45', '50', '55'], \
				'10':['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'], \
				'11':['00', '05', '10', '15', '20', '25'], \
				'13':['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'], \
				'14':['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']
				}


def print_msg(info_string):
	print "[INFO] " + info_string 

def err_msg(err_string):
	print "[ERR] " + err_string

def tradeDetailsGet(site):
	html = urllib2.urlopen(site).read()

	stock_trade = json.loads(html)
	print_msg('begin: ' + stock_trade['begin'] + ',' + 'end: ' + stock_trade['end'])
	return stock_trade['zhubi_list']
	


def tradeSiteByCode(stock_code, hour, min):
	site = "http://quotes.money.163.com/service/zhubi_ajax.html?symbol="+stock_code + "&end=" + hour + "%3A" + min + "%3A00"
	#print site
	return site



def dbFileCreate(db_name):
	print_msg("db name: " + db_name)
	if os.path.isfile(db_name) :
		#print db_name + " has already exist"
		os.remove(db_name)	
	return sqlite3.connect(db_name)

def dbTableCreate(db_connect, table_name):
	table_create_cmd = "CREATE TABLE " + table_name + " (TIME CHARACTER(20), PRICE FLOAT, VOLUME_INC INT, TRADE_TYPE INT);"
	#print table_create_cmd
	db_connect.execute(table_create_cmd)
	print_msg(table_name + " create successfully")
	return


def dbItemInsert(zhubi_list, db_conn, db_table_name):
	for zhubi in zhubi_list:
		#print "DATE_STR: %s  PRICE: %s VOLUME_INC: %s " % (zhubi["DATE_STR"], zhubi["PRICE"], zhubi["VOLUME_INC"])
		#data = zhubi["DATE_STR"]
		insert_table_cmd = "INSERT INTO " + db_table_name + " (TIME, PRICE, VOLUME_INC) VALUES (" +"\"" + zhubi["DATE_STR"] + "\"" + "," + str(zhubi["PRICE"]) +"," + str(zhubi["VOLUME_INC"]) + ")"
		#print insert_table_cmd
		db_conn.execute(insert_table_cmd)
	db_conn.commit()


def db_close(name):
	name.close() 	


def tradeItemStore(stock_code, db_connect, db_table_name):
	for k in time_key:
		for v in time_map[k]:
			site = tradeSiteByCode(stock_code, k, v)
			zhubi_list = tradeDetailsGet(site)
			dbItemInsert(zhubi_list, db_connect, db_table_name)


def tradeDataStore(stock_code):
	db_name = stock_code + '.db'
	table_name = 'TRADE_TABLE'
	db_connect = dbFileCreate(db_name)
	dbTableCreate(db_connect, table_name)
	tradeItemStore(stock_code, db_connect, table_name)
	db_close(db_connect)


stock_code = "600704"
tradeDataStore(stock_code)


def tradeInfoQuery(stock_code):
	db_name = stock_code + '.db'
	db_table_name = 'TRADE_TABLE'
	if not os.path.isfile(db_name):
		err_msg(db_name + "is not exist")
		return
	db_connect = sqlite3.connect(db_name)	
	cursor = db_connect.execute("SELECT TIME, PRICE, VOLUME_INC from " + db_table_name)	
	for row in cursor:
		print "time: %s, price %f, volume %s" %(row[0], row[1], row[2])


tradeInfoQuery(stock_code)
