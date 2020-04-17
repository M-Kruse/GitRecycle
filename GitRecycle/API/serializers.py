from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Recycler.models import Repo, Query

class RepoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repo
        #UUID is server generated, the other 4 are github repo fields that the workers need to send us.
        fields = ['uuid', 'url', 'node', 'create_date', 'description']

class QuerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Query
        fields = ['string']
