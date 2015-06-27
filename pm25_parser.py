import urllib2
from HTMLParser import HTMLParser



class PM25_HTMLParser(HTMLParser):
	def __init__(self, city_name):
		HTMLParser.__init__(self)
		self.city_name = city_name
		self.AQI_flag = False
		self.AQI_value = None
		self.PM25_flag = False
		self.PM25_Value = None
		

	def handle_starttag(self, tag, attrs):
		for attr in attrs:
			if attr[1] == "bi_aqiarea_num":
				self.AQI_flag = True
				break
			elif attr[1] == "pm25_span":
				self.PM25_flag = True

	def handle_endtag(self, tag):
		pass

	def handle_data(self, data):
		if self.AQI_flag == True:
			self.AQI_flag = False
			self.AQI_value = data
		elif self.PM25_flag == True:
			self.PM25_flag = False
			self.PM25_Value = data

	def PM25_Run(self):
		web_link = "http://www.pm25.com/" + self.city_name + ".html"
		print web_link
		html = urllib2.urlopen(web_link)
		self.feed(html.read())

	def get_PM25_AQI(self):
		return self.AQI_value

	def get_PM25_Vaule(self):
		return self.PM25_Value
	
pm25_parser = PM25_HTMLParser("beijing")
pm25_parser.PM25_Run()

print pm25_parser.get_PM25_AQI()
print pm25_parser.get_PM25_Vaule()