"""
stock trade details capture
create by royluo @ 2015.06.29
"""

import urllib2
import json
import sqlite3


end_time_slot = {'09':['35', '40', '45', '50', '55'], \
				'10':['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'], \
				'11':['00', '05', '10', '15', '20', '25'], \
				'13':['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'], \
				'14':['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']
				}


def trade_details_get(site):
	html = urllib2.urlopen(site).read()

	stock_trade = json.loads(html)
	print stock_trade['begin']
	print stock_trade['end']
	return stock_trade['zhubi_list']
	


def trade_site(stock_code):
	site = "http://quotes.money.163.com/service/zhubi_ajax.html?symbol="+stock_code + "&end=09%3A35%3A00"
	print site
	return site



def db_file_create(db_name):
	return sqlite3.connect(db_name)

def db_table_create(db_connect, table_name):
	table_create_cmd = "CREATE TABLE " + table_name + " (DATE TEXT PRIMARY KEY  NOT NULL, PRICE REAL, VOLUME INT);"
	print table_create_cmd
	db_connect.execute(table_create_cmd)
	return 0


def db_item_insert():
	pass

def db_close(name):
	pass 	

stock_code = "600704"
db_file_name = stock_code + ".db"
db_table_name = "STOCKDATA"

connect = db_file_create(db_file_name)
#db_table_create(connect, db_table_name)

site = trade_site(stock_code)

zhubi_list = trade_details_get(site)
for zhubi in zhubi_list:
	print "DATE_STR: %s  PRICE: %s VOLUME: %s TURNOVER: %s" % (zhubi["DATE_STR"], zhubi["PRICE"], zhubi["VOLUME_INC"], zhubi["TURNOVER_INC"]) 
	#insert_table_cmd = "INSERT INTO " + db_table_name + " (DATA,PRICE,VOLUME) VALUES (" + zhubi["DATE_STR"] 
	data = str(zhubi["DATE_STR"])
	insert_table_cmd = "INSERT INTO " + db_table_name + " (DATE,PRICE,VOLUME) VALUES (" +"\"" + data + "\"" + "," + str(zhubi["PRICE"]) +"," + str(zhubi["VOLUME_INC"]) + ")"

	print insert_table_cmd
	connect.execute(insert_table_cmd)

connect.commit()

connect.close()