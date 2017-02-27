import json
from requests import request

#base URL
base_url = 'https://merchant-api.jet.com/api/'

class python_jet(object):
	#snakes om a plane
	def __init__(self, jet_user, jet_secret):
		params = { 
			post_data:
				{
				"user":jet_user,
				"pass":jet_secret
				}
			}
		key_response = make_request("GET", base_url+"token", **params)
		key = key_response['id_token'].encode()
		self.auth_header = {"Authorization":key}

	def make_request(self, method, url, **kwargs):
		if post_data:
			if self.auth_header:
				r = request(method, url, data=json.dumps(post_data), headers=self.auth_header)
			else:
				r = request(method, url, data=json.dumps(post_data))
		else:
			r = request(method, url, headers=self.auth_header)

		return json.loads(r)

	def get_ready_orders():
		endpoint = '/orders/ready'
		return make_request("GET", url+endpoint)

	def print_key(self):
		print self.auth_header
		

