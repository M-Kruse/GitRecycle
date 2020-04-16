from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Recycler.models import Repo

class RepoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repo
        fields = ['url', 'node']