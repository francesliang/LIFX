import os
import requests
import lxml.html
import time
try:
    import ujson as json
except:
    import json as json

from lifx import LifxHTTP

class OlympicsMedals:

    def __init__(self):
        self.src_url = 'https://en.wikipedia.org/wiki/2016_Summer_Olympics_medal_table'
        self.table_row_xpath = ".//tr/th[@scope='row' and @align='left']"
        self.medal_counts = {}
        self.prev_medal_counts = {}

    def get_medal_info(self):
        self.prev_medal_counts = self.medal_counts.copy()
        response = requests.get(self.src_url)
        html = lxml.html.fromstring(response.text)
        tb_rows = html.xpath(self.table_row_xpath)
        for row in tb_rows:
            self.medal_counts.update(self.parse_element(row))

    def parse_element(self, element):
        medal_count = {}
        country = element.xpath('.//img/@title')[0]
        if country:
            medal_count[country] = {
                'gold':  element.getnext().text,
                'silver': element.getnext().getnext().text,
                'bronze': element.getnext().getnext().getnext().text,
                'total': element.getnext().getnext().getnext().getnext().text,
            }

        return medal_count

    def is_gold_medal(self, country):
        cur_gold = 0
        prev_gold = 0
        if self.medal_counts.get(country, None):
            cur_gold = self.medal_counts[country].get('gold', '0')
            if self.prev_medal_counts.get(country, None):
                prev_gold = self.prev_medal_counts[country].get('gold', '0')

            if cur_gold > prev_gold:
                return True
        return False


def medal_light_indicator(light, token):

    lifx =LifxHTTP(token)
    medals = OlympicsMedals()

    #medals.get_medal_info()

    while True:
        medals.get_medal_info()
        if medals.is_gold_medal('China'):
            print 'China won a gold medal!'
            lifx.set_pulse_effect('light_name', 'red', selector_val=light, from_color=None, period=0.4, cycles=5,
                          persist=False, power_on=True)
        time.sleep(2)
        if medals.is_gold_medal('Australia'):
            print 'Australia won a gold medal!'
            lifx.set_pulse_effect('light_name', 'yellow', selector_val=light, from_color=None, period=0.4, cycles=5,
                          persist=False, power_on=True)





