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
		#check time auth_header was saved, use in new definition
		#to figure out if it's close to expiring; request new key

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

		try:
			return json.loads(r.text)
		except ValueError:
			return r.text
			#request_exec = r.text
			#raise request_exec

	def build_request(self, url, alt_order_id, arr_name):
		#to-do		

	#orders API

	def check_for_orders(self, status):
		endpoint = '/orders/%s' % status
		return self.make_request("GET", endpoint)['order_urls']

	def check_order_details_by_url(self, order_url):
		return self.make_request("GET", order_url)

	def ack_order(self, jet_order_id, ack_status, order_items, alt_order_id=None):
		#Reference: https://developer.jet.com/docs/acknowledge-order
		ack_url = "/orders/%s/acknowledge" % jet_order_id
		post_data = {}
		order_item_data = {}

		order_item_data.update({"acknowledgement_status": ack_status})
		if alt_order_id:
			order_item_data.update({"alt_order_id": alt_order_id})
		order_item_data.update({"order_items": order_items})
		#order_items must be a list of dicts
		#[{
		#	"order_item_acknowledgement_status": "fulfillable",
		#	"order_item_id": "8f5ae15b6b414b00a1b9d6ad99166a00",
		#	"alt_order_item_id": "76-i105"
		#}]
		params = {"post_data" : order_item_data}
		return self.make_request("PUT", ack_url, **params)

	def ship_orders(self, jet_order_id, alt_order_id, shipments_array):
		#Reference: https://developer.jet.com/docs/ship-order
		ship_url = "/orders/%s/shipped" % jet_order_id
		post_data = {}
		shipment_data = {}

		shipment_data.update({"shipments": shipments_array})
		if alt_order_id:
			shipment_data.update({"alt_order_id": alt_order_id})
		#shipments must be a list of dicts
		#[{
		#	"alt_shipment_id": "12345",
		#	"shipment_tracking_number": "1zxy67934234098",
		#}]
		params = {"post_data" : shipment_data}
		return self.make_request("PUT", ship_url, **params)

	def tag_order(self, jet_order_id, tag_string):
		#Reference: https://developer.jet.com/docs/tag-order
		tag_url = "/orders/%s/tag" % jet_order_id
		post_data = {}
		tag_data = {}

		tag_data.update({"tag": tag_string})
		params = {"post_data" : tag_data}
		return self.make_request("PUT", tag_url, **params)

	#def print_key(self):
	#	return self.auth_header


