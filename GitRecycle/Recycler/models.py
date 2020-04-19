from django.db import models

from datetime import datetime, timedelta
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator

class Query(models.Model):
    string = models.CharField(max_length=64) #The search query used to find the repos
    language = models.CharField(max_length=64, blank=True, null=True) #The language you want to search for
    time_limit_seconds = models.IntegerField( #Time limit before we consider the repo to be stale and not interesting anymore
                                    default=300, #This should probably be tiered so that projects deleted quickly have higher alert level
                                    validators=[
                                        MaxValueValidator(86400), #24 hour max
                                        MinValueValidator(10)
                                        ]
                                )
    def __str__(self):
        return self.string

class Repo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4) #Node ID might be unique enough to be used as a unique id
    query = models.ForeignKey('Query', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=512, null=True)
    url =  models.CharField(max_length=256) # 'html_url': 'https://github.com/daniel-e/tetros',
    node = models.CharField(max_length=256, unique=True, primary_key=True) # 'node_id': 'MDEwOlJlcG9zaXRvcnk2ODkxMTY4Mw==',GraphQL node_id - can try integrating GraphQL
    create_date = models.CharField(max_length=128, null=True) #  '2016-09-22T10:42:55Z', When the repo was created
    scrape_date = models.DateTimeField(default=datetime.now) #  When we scraped the repo
    last_checked = models.DateTimeField(null=True) # '2016-09-22T10:42:55Z',
    stale = models.BooleanField(default=False) #Set this to true after a time limit so it won't be checked anymore, then remove the archive
    archived = models.BooleanField(default=True) #By default we save the repo before creating new Repo object so it will be True until it is removed from storage
    stale_date = models.DateTimeField(null=True)
    archive_loc = models.CharField(max_length=512, default="")

    def __str__(self):
        return self.url

class MissingRepo(models.Model):
    #origin_repo = models.UUIDField(null=True) #Node ID might be unique enough to be used as a unique id
    origin_repo = models.ForeignKey('Repo', on_delete=models.SET_NULL, null=True) #I'm not sure if this is really necessary
    date_found = models.DateTimeField(auto_now_add=True) # '2016-09-22T10:42:55Z',
    is_interesting = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    def __str__(self):
        return str(self.origin_repo)
