
# System Imports
import pyqrcode
import sys
import io

# Django Imports
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import generics


# User Imports
from shop.models import Product, Order, OrderItem
from shop.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
# import django_filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import DetailView


# async def websocket_view(socket: WebSocket):
# 	await socket.accept()
# 	while True:
# 		message = await socket.receive_text()
# 		await socket.send_text(message)


# class BorrowedFilterSet(filters.FilterSet):
#    missing = filters.UUIDFilterfield_name='order_id', lookup_expr='exact')

#    class Meta:
#        model = Order
#        fields = ['order_id']

class ActionBasedPermission(AllowAny):
	"""
	Grant or deny access to a view, based on a mapping in view.action_permissions
	"""
	def has_permission(self, request, view):
		for klass, actions in getattr(view, 'action_permissions', {}).items():
			if view.action in actions:
				return klass().has_permission(request, view)
		return False

class ProductViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	print("Using Product ViewSet")
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	# permission_classes = [permissions.IsAuthenticated]
	permission_classes = (ActionBasedPermission,)
	action_permissions = {
		IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'retrieve'],
		AllowAny: ['list','retrieve']
	}


class OrderViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	# class Meta:
	model = Order
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	action_permissions = {
		IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'retrieve','list',],
		AllowAny: ['retrieve']
	}
	# filter_backends = [DjangoFilterBackend]
	# filterset_fields = ('order_id')

	# def get_queryset(self):
	# 	queryset = self.queryset
	# 	oid = self.request.query_params.get('order_id', None)
	# 	print(oid)
	# 	if oid is not None:
	# 		queryset = queryset.filter(order_id=oid)
	# 	return query_set


class OrderItemViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	action_permissions = {
		IsAdminUser: ['update', 'partial_update', 'destroy', 'create', 'retrieve','list',],
		AllowAny: ['retrieve']
	}

def index(request):
	return HttpResponse("Hello, world. You're at the shop index. <br/><br/> <img src='qrcode?data=testing1234'/>")

def qrcode(request):
	qrdata = request.GET['data']
	code = pyqrcode.create(qrdata)
	image_as_str = code.png_as_base64_str(scale=10)
	with io.BytesIO() as virtual_file:
		code.png(file=virtual_file, scale=10)
		virtual_file.getvalue()
	# qrhtml = f'<img src="data:image/png;base64, {image_as_str}">'
		return HttpResponse(virtual_file.getvalue(),content_type="image/png")




class CheckOrderStatus(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Order.objects.all()
        oid = self.request.query_params.get('order_id', None)
        if oid is not None:
            queryset = queryset.filter(order_id=oid)
        return queryset

class CheckOrderDetailView(generics.RetrieveAPIView):
	# queryset = Order.objects.all()
	model = Order
	slug_field = "order_id"
	# lookup_field = "order_id"
	slug_url_kwarg = "order_id"

	# def get_object(self):
	# 	obj = super().get_object()
	# 	# Record the last accessed date
	# 	# obj.last_accessed = timezone.now()
	# 	print(obj)
	# 	obj.save()
	# 	return obj
		
