# snakesonaplane - a Python Interface for the Jet developer API

This project is a work in progress! Use at your own risk for integrating with Jet. When making a pull request, please use tabs!

### Usage

Simply import the module and create a new jet object:

```
from snakesonaplane import jet

jet_user = "USER_KEY"
jet_secret = "SECRET_KEY"

j = jet(jet_user,jet_secret)
```
...and use the object to work with the API:

```
#acknowledge new orders on Jet
for url in j.get_ready_order_urls():
	order_details = j.get_order_details_by_url(url)
	order_id = order_details['merchant_order_id']
	order_items = order_details['order_items']

	fulfillable_items = []
	for order_item in order_items:
		fulfillable_items.append({
		"order_item_acknowledgement_status": "fulfillable",
		"order_item_id": order_item['order_item_id']
		})
	print j.ack_order(order_id, "accepted", fulfillable_items)
```  

### To-do
 - finish adding all API calls
 - token timeouts
