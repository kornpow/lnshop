from django.db import models
import uuid
from lnpanda import lnpanda
from datetime import datetime
import requests

ln = lnpanda()

class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.FloatField()
	product_image = models.ImageField(upload_to='images/')
	supplier = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class OrderItem(models.Model):
	# ,related_name='orderitem
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.product.name} X {self.quantity}"

class Order(models.Model):
	# order_uuid = models.UUIDField(default=uuid4, blank=True, null=True)
	order_uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
	ship_address = models.CharField(max_length=200)
	created_at = models.DateTimeField(default=datetime.now)
	paid = models.BooleanField(default=False)
	shipped = models.BooleanField(default=False)
	payment_request = models.CharField(max_length=262,blank=True)
	items = models.ManyToManyField(OrderItem, blank=True, related_name="orders")
	sats_per_dollar = models.IntegerField(null=False, default=0)
	price_sats = models.IntegerField(null=False, default=0)
	shipping_fee_usd = models.DecimalField(null=False, max_digits=5, decimal_places=2)
	

	def __str__(self):
		return f'{self.order_uuid.hex} --> Paid/Shipped: {self.paid}/{self.shipped}'

	def get_btc_price(self):
		sats = int(requests.get('https://blockchain.info/tobtc?currency=USD&value=1').json() * 100000000)
		print(f"Using {sats} sat/$")
		return sats

	def get_invoice(self,sats,invoice_string):
		# result = addInvoice(sats,f'ChaosNCoffee \n {invoice_string}')['payment_request']
		# TODO: MIGRATE
		result = ln.lnd.add_invoice(value=sats, memo=f'ChaosNCoffee \n {invoice_string}').payment_request
		return result

	def get_order_amt(self):
		total_price_usd = 0
		for item in self.items.values():
			quantity = item['quantity']
			product = Product.objects.get(id=item['product_id'])
			total_price_usd += product.price * quantity
		return total_price_usd

	def save(self, *args, **kwargs):
		if self.payment_request == '':
			self.sats_per_dollar = self.get_btc_price()
			# order_dollars = self.get_order_amt()
			print("Generating a payment request!")
			self.payment_request = self.get_invoice(self.sats_per_dollar, 'test_shop')
		else:
			print("Payment request already exists!")
		print(self.payment_request)
		super(Order, self).save(*args, **kwargs)
		# print(self.items.values())
	

from django.db.models.signals import m2m_changed

def toppings_changed(sender,instance, **kwargs):
	print('Order Saved')
	# print()
	# total_price_usd = 0
	# Get USD Price
	total_price_usd = instance.get_order_amt()
	# for item in instance.items.values():
	# 	quantity = item['quantity']
	# 	product = Product.objects.get(id=item['product_id'])
	# 	total_price_usd += product.price * quantity
	# Convert to price in sats
	# print(instance.)

	# Start here:
	order_list = []
	order_items = instance.items.values_list()
	for item in order_items:
		product_name = Product.objects.get(id=item[1]).name
		quantity = item[2]
		order_list.append(f"\n{product_name}: {quantity}")
	order_string = ', '.join(order_list)
	
	total_price_sats = int(total_price_usd * instance.sats_per_dollar)
	instance.price_sats = total_price_sats
	instance.payment_request = instance.get_invoice(total_price_sats,order_string)
	print("Saving created invoice!")
	instance.save()

m2m_changed.connect(toppings_changed, sender=Order.items.through)