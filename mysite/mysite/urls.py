"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import include, re_path
from rest_framework import routers
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
# from websocket.urls import websocket


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
# router.register(r'orders/(?P<order_id>.+)/$', views.OrderViewSet)

router.register(r'orderitems', views.OrderItemViewSet)

urlpatterns = [
	path('shop/', include('shop.urls')),
	path('admin/', admin.site.urls),
	path('', include(router.urls)),
	# path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    # api
    # url(r'^api/v1/posts/$', views.PostCollection.as_view()),
    # url(r'^api/v1/posts/(?P<pk>[0-9]+)/$', views.PostMember.as_view())
    # url(r'^order/status/$', views.CheckOrderStatus.as_view()),
	path(r'orders/<order_id>', views.CheckOrderDetailView.as_view(), name='order-detail'),
    # url(r'^api/v1/posts/(?P<pk>[0-9]+)/$', views.PostMember.as_view())

	# WEB SOCKETS?
	# websocket("ws/", views.websocket_view)
	re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
	re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
