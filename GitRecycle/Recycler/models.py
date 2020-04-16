from django.db import models
import uuid

class Query(models.Model):
	string = models.CharField(max_length=64) #The search query used to find the repos 

class Repo(models.Model):
	#uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	query = models.ForeignKey('Query', on_delete=models.DO_NOTHING, null=True)
	url =  models.CharField(max_length=254) # 'html_url': 'https://github.com/daniel-e/tetros',
	node = models.CharField(max_length=254) # 'node_id': 'MDEwOlJlcG9zaXRvcnk2ODkxMTY4Mw==',
	create_date = models.DateTimeField(auto_now_add=True, editable=False) #  '2016-09-22T10:42:55Z',
	last_checked = models.DateTimeField(null=True) # '2016-09-22T10:42:55Z',
	stale = models.BooleanField(default=False) #Set this to true after a time limit so it won't be checked anymore

class DeletedRepo(models.Model):
	repo = models.ForeignKey('Repo', on_delete=models.DO_NOTHING)
	date_found = models.DateTimeField(auto_now_add=True) # '2016-09-22T10:42:55Z',
	is_interesting = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	note = models.TextField()
