from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Recycler.models import Repo, Query, MissingRepo

class RepoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repo
        fields = ['uuid', 'url', 'node', 'create_date', 'description', 'stale', 'last_checked', 'missing', 'archived', 'archive_loc']

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(RepoSerializer, self).get_serializer(*args, **kwargs)

class QuerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Query
        fields = ['string', 'language', 'last_searched']

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(QuerySerializer, self).get_serializer(*args, **kwargs)

class MissingRepoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MissingRepo
        fields = ['origin_repo']
