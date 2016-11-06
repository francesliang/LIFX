import os
import sys
from datetime import datetime

from lifx import LifxHTTP
from forecast_io import ForecastIO

class LifeBulb:

	def __init__(self, lifx_token):

		self.lifx = LifxHTTP(lifx_token)

	### Weather indicator
	def indicate_weather(self, key, light='Bedroom', city='Brisbane', max_temp=30, precip_prob=0.5, precip_type='rain'):
		forecastIO = ForecastIO(key)
		forecastIO.get_weather_data(city)
		today = forecastIO.get_daily_weather().get(datetime.now().strftime(forecastIO.date_format()))

		if today:
			color1 = 'white'
			color2 = 'white'
			if today.get('temperatureMax', 0) > max_temp:
				color1 = 'red'
			if today.get('precipProbability', 0.0) > precip_prob and today.get('precipType', '') == precip_type:
				color2 = 'blue'

			self.lifx.set_pulse_effect(color1, selector='light', selector_val=light, from_color=color2, period=1.0, cycles=10.0,
	                          persist=False, power_on=True)
		else:
			print "No weather data available."

	### Special occasions
	def indicate_special_date(self, light, colour_1, colour_2='white', special_date='25 Dec', date_format='%d %b'):
		occasion = datetime.strptime(special_date, date_format)
		today = datetime.now()
		if today.month == occasion.month and today.day == occasion.day:
			self.lifx.set_pulse_effect(colour_1, selector='light', selector_val=light, from_color=colour_2, period=1.0, cycles=10.0,
		                          persist=False, power_on=True)



if __name__ == '__main__':

	lifx_token = sys.argv[1]
	forecast_io_key = sys.argv[2]

	bulb = LifeBulb(lifx_token)
	bulb.indicate_weather(forecast_io_key)



