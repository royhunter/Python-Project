"""
stock trade details capture
create by royluo @ 2015.06.29
"""

import urllib2
import json



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
	for zhubi in stock_trade['zhubi_list']:
		print "DATE_STR: %s  PRICE: %s VOLUME: %s TURNOVER: %s" % (zhubi["DATE_STR"], zhubi["PRICE"], zhubi["VOLUME_INC"], zhubi["TURNOVER_INC"])


def trade_site(stock_code):
	site = "http://quotes.money.163.com/service/zhubi_ajax.html?symbol="+stock_code + "&end=09%3A35%3A00"
	print site
	return site




site = trade_site("600704")

trade_details_get(site)

