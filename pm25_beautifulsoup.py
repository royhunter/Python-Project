#-*-coding:utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import sys


def getPM25(cityname):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	site = "http://www.pm25.com/" + cityname + ".html"
	html = urllib2.urlopen(site)
	soup = BeautifulSoup(html)

	city = soup.find(class_="bi_loaction_city")
	print city.text
	aqi = soup.find(class_="bi_aqiarea_num") 
	print aqi.text
	air_level = soup.find(class_="bi_aqiarea_wuran")
	print air_level.text
	result = soup.find(class_="bi_aqiarea_bottom")
	print result.text

getPM25("tianjin")