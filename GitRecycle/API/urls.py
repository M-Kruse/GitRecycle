from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'stale', views.StaleRepoViewSet)
router.register(r'fresh', views.FreshRepoViewSet)
router.register(r'', views.RepoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('repo/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]