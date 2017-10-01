import os
import sys
from datetime import datetime
import time

from lifx import LifxHTTP
from utils.forecast_io import ForecastIO
from utils.detect_network import check_device_in_net_nmap

class LifeBulb:

	def __init__(self, lifx_token):

		self.lifx = LifxHTTP(lifx_token)

	### Weather indicator
	def indicate_weather(self, key, light='Bedroom', city='Brisbane', temp_thresh=30, precip_thresh=0.5, precip_type='rain'):
		forecastIO = ForecastIO(key)
		forecastIO.get_weather_data(city)
		today = forecastIO.get_daily_weather().get(datetime.now().strftime(forecastIO.date_format()))

		if today:
			color1 = 'white'
			color2 = 'white'
			temp = today.get('temperatureMax', 0)
			precip = today.get('precipProbability', 0.0)
			if  temp > temp_thresh:
				color1 = 'rgb:255,0,0 brightness:0.75 saturation:' + str(float(temp)/temp_thresh-0.4)
			if precip > precip_thresh and today.get('precipType', '') == precip_type:
				color2 = 'rgb:0,0,255 brightness:0.75 saturation:' + str(precip)

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

	
	### Turn on lounge light when home after sun-set
	def return_home_light(self, mac_addr, start_hour=18, light='LivingRoom1'):
		start_t = time.time()
		end_t = start_t
		t_thresh = 180

		while not check_device_in_net_nmap(mac_addr):
			end_t = time.time()

		t_now = datetime.now().time().hour
		if t_now >= start_time:
			if check_device_in_net_nmap and (end_t-start_t)>t_thresh:
				self.set_state('power', 1, selector_val=light)
		


if __name__ == '__main__':

	lifx_token = sys.argv[1]
	forecast_io_key = sys.argv[2]

	bulb = LifeBulb(lifx_token)
	bulb.indicate_weather(forecast_io_key)



