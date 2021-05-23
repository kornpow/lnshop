from rest_framework import serializers
from django_restql.serializers import NestedModelSerializer
from django_restql.fields import NestedField
from django_restql.mixins import DynamicFieldsMixin
from shop.models import Product, Order, OrderItem

# DynamicFieldsMixin,
class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = [
			'id', 'name', 'description', 'price', 'product_image', 'supplier'
		]

# DynamicFieldsMixin,
class OrderItemSerializer(NestedModelSerializer):
	product = NestedField(ProductSerializer, accept_pk=True)
	class Meta:
		model = OrderItem
		fields = [
			'id','quantity','product'
		]


class OrderSerializer(DynamicFieldsMixin,NestedModelSerializer):
	items = NestedField(OrderItemSerializer, 
		many=True, 
		required=True,
		create_ops=["add","create"],
	)

	class Meta:
		model = Order
		# fields = ['order_id','items']
		fields = '__all__'


