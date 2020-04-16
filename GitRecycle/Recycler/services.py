#Get the queries from the database
#Search github
#Use results to find and save new repos
#Use results to find deleted repos against saved
#Generate alerts for deleted repos

#Should figure out how to implement with a ServiceMetaclass - https://github.com/mixxorz/django-service-objects/blob/master/service_objects/services.py

from .models import Repo

def set_repo_stale(pk):
	pass

def is_new_repo(repo_url, node_id):
	return False

def archive_repo(pk):
	pass

def delete_repo(pk):
	pass

def generate_alert(pk):
	pass