from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import RepoSerializer, QuerySerializer

from Recycler.models import Repo, Query

from django.conf import settings as conf_settings

class RepoViewSet(viewsets.ModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ArchivedRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(archived=True)
    serializer_class = RepoSerializer

class StaleRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(stale=True)
    serializer_class = RepoSerializer

class FreshRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(stale=False)
    serializer_class = RepoSerializer

class QueryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

class RoundRobinQueryViewSet(viewsets.ReadOnlyModelViewSet):
    conf_settings.RR_INDEX = 0
    queryset = Query.objects.all()
    #This is my little hack to make it round-robin through the queries, don't judge me
    def list(self, request):    
        query_count = Query.objects.count()
        if conf_settings.RR_INDEX < query_count - 1:
            conf_settings.RR_INDEX += 1
        else:
            conf_settings.RR_INDEX = 0
        queryset = Query.objects.all()[conf_settings.RR_INDEX]
        print(queryset)
        serializer = QuerySerializer(queryset)
        return Response(serializer.data)
    
