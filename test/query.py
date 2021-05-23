import requests
from pprint import pprint

port = 12345
hostname = 'http://localhost'
# hostname = 'http://3.15.138.122'
host = f'{hostname}:{port}'
host = "https://api.btcmemes.com"

# Get product list
products = requests.get(f"{host}/products/").json()
pprint(products)

# Create a new order item
order_item = requests.post("",json={'quantity':5,'product':1}).json()
pprint(order_item)

# Create a new order
order = requests.post(f"{host}/orders/",json={'ship_address':'tesst 1234','items':{'create':[{'quantity':5,'product':1}]}}).json()

order = requests.post(f"{host}/orders/",json={'ship_address':'8624 Plaza 31, Democrat, Michigan, 22310','items':{'create':[{'quantity':1,'product':9},{'quantity':1,'product':12}]}}).json()

pprint(order)

# Make QR Code
url = f"{host}/shop/qrcode?data={ order['payment_request'] }"