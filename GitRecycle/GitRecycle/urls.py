from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/', include('API.urls')),
	path('api-token-auth/', obtain_auth_token, name='api-tokn-auth'), 
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]