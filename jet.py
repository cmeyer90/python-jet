import json
from datetime import datetime
from requests import request
import dateutil.parser

class Jet(object):
    def __init__(self, jet_user, jet_secret):
        self.auth_header = False
        self.base_url = 'https://merchant-api.jet.com/api'
        self.params = { 
            "post_data":
                {
                "user":jet_user,
                "pass":jet_secret
                }
            }
        self.get_auth_header()

    def check_time_to_live_decorator(self, func):
        def wrapper():
            if datetime.utcnow() > self.expires_on:
                get_auth_header()
            func()
        return wrapper
        
    def get_auth_header():
        self.key_response = self.make_request("POST", "/token", **self.params)
        self.key = key_response['id_token'].encode()
        self.expires_on = dateutil.parser.parse(key_response['expires_on'].encode()).replace(tzinfo=None)
        self.token_type = key_response['token_type'].encode()
        self.auth_header = {"Authorization":"{self.token_type} {self.key}".format(**locals())}

    @check_time_to_live_decorator
    def make_request(self, method, url, **kwargs):
        if "post_data" in kwargs:
            post_data = kwargs['post_data']
            if self.auth_header:
                r = request(method, self.base_url + url, data=json.dumps(post_data), headers=self.auth_header)
            else:
                r = request(method, self.base_url + url, data=json.dumps(post_data))
        else:
            r = request(method, self.base_url + url, headers=self.auth_header)

        try:
            return json.loads(r.text)
        except ValueError:
            return r.text
            #request_exec = r.text
            #raise request_exec
            
    @check_time_to_live_decorator
    def build_request(self, url, alt_order_id, arr_name):
        pass
        #to-do        

    #orders API
    @check_time_to_live_decorator
    def check_for_orders(self, status):
        endpoint = '/orders/{status}'.format(**locals())
        return self.make_request("GET", endpoint)['order_urls']
        
    @check_time_to_live_decorator
    def check_order_details_by_url(self, order_url):
        return self.make_request("GET", order_url)
        
    @check_time_to_live_decorator
    def ack_order(self, jet_order_id, ack_status, order_items, alt_order_id=None):
        #Reference: https://developer.jet.com/docs/acknowledge-order
        ack_url = "/orders/{jet_order_id}/acknowledge".format(**locals())
        order_item_data = {
            "acknowledgement_status": ack_status,
            "order_items": order_items
            }
        if alt_order_id:
            order_item_data.update({"alt_order_id": alt_order_id})
        #order_items must be a list of dicts
        #[{
        #    "order_item_acknowledgement_status": "fulfillable",
        #    "order_item_id": "8f5ae15b6b414b00a1b9d6ad99166a00",
        #    "alt_order_item_id": "76-i105"
        #}]
        params = {"post_data" : order_item_data}
        return self.make_request("PUT", ack_url, **params)
        
    @check_time_to_live_decorator
    def ship_orders(self, jet_order_id, alt_order_id, shipments_array):
        #Reference: https://developer.jet.com/docs/ship-order
        ship_url = "/orders/{jet_order_id}/shipped".format(**locals())
        shipment_data = {"shipments": shipments_array}
        if alt_order_id:
            shipment_data.update({"alt_order_id": alt_order_id})
        #shipments must be a list of dicts
        #[{
        #    "alt_shipment_id": "12345",
        #    "shipment_tracking_number": "1zxy67934234098",
        #}]
        params = {"post_data" : shipment_data}
        return self.make_request("PUT", ship_url, **params)
        
    @check_time_to_live_decorator
    def tag_order(self, jet_order_id, tag_string):
        #Reference: https://developer.jet.com/docs/tag-order
        tag_url = "/orders/{jet_order_id}/tag".format(**locals())
        tag_data = {"tag": tag_string}
        params = {"post_data" : tag_data}
        return self.make_request("PUT", tag_url, **params)

    #def print_key(self):
    #    return self.auth_header
