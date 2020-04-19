from django.urls import include, path
from rest_framework import routers
from . import views

repo_router = routers.DefaultRouter()
repo_router.register(r'stale', views.StaleRepoViewSet)
repo_router.register(r'fresh', views.FreshRepoViewSet)
repo_router.register(r'worker', views.CycleFreshRepoViewSet)
repo_router.register(r'missing', views.MissingRepoViewSet)
#repo_router.register(r'(?P<slug>[\w-]+)/', views.RepoNodeQueryViewSet)
repo_router.register(r'', views.RepoViewSet)

query_router = routers.DefaultRouter()
query_router.register(r'worker', views.CycleQueryViewSet)
query_router.register(r'', views.QueryViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('repo/', include(repo_router.urls)),
    path('query/', include(query_router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]