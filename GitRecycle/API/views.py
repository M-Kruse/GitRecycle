from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from .serializers import RepoSerializer, QuerySerializer, MissingRepoSerializer

from Recycler.models import Repo, Query, MissingRepo

from django.conf import settings as conf_settings
from datetime import datetime, timedelta

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

class CycleQueryViewSet(viewsets.ReadOnlyModelViewSet):
    conf_settings.RRQ_INDEX = 0
    queryset = Query.objects.all()
    #This is my little hack to make it cycle through the queries, don't judge me
    def list(self, request):    
        query_count = Query.objects.count()
        if conf_settings.RRQ_INDEX < query_count - 1:
            conf_settings.RRQ_INDEX += 1
        else:
            conf_settings.RRQ_INDEX = 0
        queryset = Query.objects.all()[conf_settings.RRQ_INDEX]
        serializer = QuerySerializer(queryset)
        return Response(serializer.data)
from django.utils import timezone
import pytz
class CycleFreshRepoViewSet(viewsets.ReadOnlyModelViewSet):
    conf_settings.RRR_INDEX = 0
    queryset = Repo.objects.filter(stale=False)
    #This is my little hack to make it cycle through the queries, don't judge me
    def list(self, request):
        query_count = Repo.objects.count()
        if conf_settings.RRR_INDEX < query_count - 1:
            conf_settings.RRR_INDEX += 1
        else:
            conf_settings.RRR_INDEX = 0
        now = datetime.now()
        print(now.strftime('%Y-%m-%dT%H:%M:%S%z'))
        time_threshold = now - timedelta(seconds=30)
        #print(time_threshold.strftime('%Y-%m-%dT%H:%M:%S%z'))
        queryset = Repo.objects.filter(stale=False, last_checked__lt=time_threshold)[conf_settings.RRR_INDEX]
        # if len(queryset) == 0:
        #     return Response()
        # else:
        #     if len(queryset) > 1:
        #         queryset = queryset[conf_settings.RRR_INDEX]
        #     print(queryset)
        #     print(len(queryset))
        print(queryset)
        serializer = RepoSerializer(queryset)
        return Response(serializer.data)
    
class MissingRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MissingRepo.objects.filter()
    serializer_class = MissingRepoSerializer

class RepoNodeQueryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MissingRepo.objects.all()
    serializer_class = MissingRepoSerializer
    lookup_field = 'nodeID'
