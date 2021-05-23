import django_filters

from shop.models import Product, Order, OrderItem

class FilmFilter(django_filters.FilterSet):
	class Meta:
		model = Order