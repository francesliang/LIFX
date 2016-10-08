import requests
import traceback

from selectors import Selectors


class LifxHTTP:

    def __init__(self, token):
        self.base_url = "https://api.lifx.com/v1/lights/"
        self.token = token
        self.headers = {
            "Authorization": "Bearer %s" % self.token,
        }

    def request_base(self, req_type, selector, selector_val=None, func='', payload=None):
        if selector_val:
            url = self.base_url + Selectors.get(selector, 'all') + ':' + selector_val + '/' + func
        else:
            url = self.base_url + Selectors.get(selector, 'all') + '/' + func

        if req_type.lower() == 'put':
            response = requests.put(url, data=payload, headers=self.headers)
        elif req_type.lower() == 'get':
            response = requests.get(url, data=payload, headers=self.headers)
        elif req_type.lower() == 'post':
            response = requests.post(url, data=payload, headers=self.headers)
        return response.json()

    def check_results(self, response):
        results = response.get('results', None)
        if results:
            if all(r.get('status', '') == 'ok' for r in results):
                return True
            else:
                print results
        return False

    def get_status(self, selector, selector_val=None):
        try:
            response = self.request_base('get', selector, selector_val)
            return response
        except Exception as e:
            print "Error at get_status %s" % e
            traceback.print_exc()
            return []

    def set_state(self, selector, state, state_val, selector_val=None):
        # state - power, color, brightness, duration
        try:
            func = 'state'
            payload = {
                state: state_val,
            }
            response = self.request_base('put', selector, selector_val, func, payload)
            return self.check_results(response)
        except Exception as e:
            print "Error at set_state %s" % e
            traceback.print_exc()
            return False

    def toggle_power(self, selector, selector_val=None, duration=1.0):
        try:
            func = 'toggle'
            payload = {
                'duration': str(duration),
            }
            response = self.request_base('post', selector, selector_val, func, payload)
            return self.check_results(response)
        except Exception as e:
            print "Error at toggle_power %s" % e
            traceback.print_exc()
            return False

    def set_breathe_effect(self, selector, color, selector_val=None, from_color=None, period=1.0, cycles=1.0,
                          persist=False, power_on=True, peak=0.5):
        try:
            func = 'effects/breathe'
            payload = {
                'color': color,
                'from_color': from_color,
                'period': period,
                'cycles': cycles,
                'persist': persist,
                'power_on': power_on,
                'peak': peak,
            }
            response = self.request_base('post', selector, selector_val, func, payload)
            return self.check_results(response)
        except Exception as e:
            print "Error at set_breathe_effect %s" % e
            traceback.print_exc()
            return False

    def set_pulse_effect(self, selector, color, selector_val=None, from_color=None, period=1.0, cycles=1.0,
                          persist=False, power_on=True):
        try:
            func = 'effects/pulse'
            payload = {
                'color': color,
                'from_color': from_color,
                'period': period,
                'cycles': cycles,
                'persist': persist,
                'power_on': power_on,
            }
            response = self.request_base('post', selector, selector_val, func, payload)
            return self.check_results(response)
        except Exception as e:
            print "Error at set_pulse_effect %s" % e
            traceback.print_exc()
            return False

    def validate_color(self, color_string):
        try:
            url = 'https://api.lifx.com/v1/color'
            payload = {
                'string': color_string,
            }
            response = requests.get(url, data=payload, headers=self.headers)
            return response
        except Exception as e:
            print "Error at validate_color %s" % e
            traceback.print_exc()
            return []

    #TODO
    # set states
    # scenes






