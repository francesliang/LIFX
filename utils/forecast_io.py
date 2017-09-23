import requests
import sys
import json
from urllib import urlencode
from datetime import datetime
import operator
from collections import OrderedDict
import traceback

from geopy.geocoders import Nominatim


class ForecastIO:

	forecast_url = 'https://api.darksky.net/forecast/%s/%s,%s?%s'

	def __init__(self, key):
		self.key = key
		self.request_url = ''
		self.geolocator = Nominatim()
		self.data = None

	def generate_request_url(self, lat, longt, exclude='', extend='', lang='', units='si'):
		self.request_url = ''

		url_args = {
			'exclude': exclude,
			'extend': extend,
			'lang': lang,
			'units': units
		}
		self.request_url = self.forecast_url % (str(self.key),  str(lat),  str(longt), urlencode(url_args))

	def get_weather_data(self, city):
		location = self.geolocator.geocode(city)
		self.generate_request_url(location.latitude, location.longitude, units='si')
		res = requests.get(self.request_url)
		if res.status_code == 200:
			self.data = res.json()
			return res.json()
		else:
			return None

	def get_current_weather(self):
		current = self.data.get('currently', None)
		if current:
			current['time'] = datetime.fromtimestamp(current.get('time', None)).strftime('%Y-%m-%d %H:%M:%S')
		return current

	def get_daily_weather(self):
		daily = dict()

		days = self.data.get('daily', {}).get('data', None)
		if days:
			for day in days:
				day['time'] = datetime.fromtimestamp(day.get('time', None)).strftime('%Y-%m-%d')
				daily[day.get('time')] = day

		daily = OrderedDict(sorted(daily.items()))

		return daily

	def date_format(self):
		return '%Y-%m-%d'


if __name__ == '__main__':

	key = sys.argv[1]
	city = sys.argv[2]

	forecastIO = ForecastIO(key)
	forecastIO.get_weather_data(city)
	print json.dumps(forecastIO.get_current_weather(), indent=4)


