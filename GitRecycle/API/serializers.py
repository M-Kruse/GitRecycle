from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Recycler.models import Repo, Query

class RepoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repo
        fields = ['uuid', 'url', 'node', 'create_date', 'description', 'stale']
        
    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(RepoSerializer, self).get_serializer(*args, **kwargs)

class QuerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Query
        fields = ['string', 'language']
