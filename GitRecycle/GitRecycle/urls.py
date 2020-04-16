from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    
	path('api/', include('API.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]