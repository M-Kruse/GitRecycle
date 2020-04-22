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

class MissingRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(missing=True)
    serializer_class = RepoSerializer
