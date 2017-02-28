import json
from requests import request

#base URL
base_url = 'https://merchant-api.jet.com/api'

class jet(object):
	#snakes on a plane
	def __init__(self, jet_user, jet_secret):
		self.auth_header = False
		params = { 
			"post_data":
				{
				"user":jet_user,
				"pass":jet_secret
				}
			}
		key_response = self.make_request("POST", "/token", **params)
		key = key_response['id_token'].encode()
		self.auth_header = {"Authorization":"Bearer %s" % key}

	def make_request(self, method, url, **kwargs):
		url = base_url + url
		if "post_data" in kwargs:
			post_data = kwargs['post_data']
			if self.auth_header:
				r = request(method, url, data=json.dumps(post_data), headers=self.auth_header)
			else:
				r = request(method, url, data=json.dumps(post_data))
		else:
			r = request(method, url, headers=self.auth_header)
		return json.loads(r.text)

	def get_ready_order_urls(self):
		endpoint = '/orders/ready'
		return self.make_request("GET", endpoint)['order_urls']

	def get_order_details_by_url(self, order_url):
		return self.make_request("GET", order_url)

	def print_key(self):
		return self.auth_header


