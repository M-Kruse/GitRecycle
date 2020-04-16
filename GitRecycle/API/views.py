from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import RepoSerializer
from Recycler.models import Repo
from rest_framework.decorators import api_view

class RepoViewSet(viewsets.ModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArchivedRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(archived=True)
    serializer_class = RepoSerializer

class StaleRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(stale=True)
    serializer_class = RepoSerializer

class FreshRepoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.filter(stale=False)
    serializer_class = RepoSerializer