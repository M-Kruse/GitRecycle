from django.urls import reverse

from git import Git, Repo
from git.exc import InvalidGitRepositoryError

from celery import task, shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from Recycler import models

import requests

from datetime import datetime, timedelta

import pytz

archive_path = "/mnt/Personal/ApplicationData/GitRecycle/archives/"
github_search_url = "https://api.github.com/search/repositories"

@shared_task()
def clone_repo(repo_pk):
        repo = models.Repo.objects.get(pk=repo_pk)
        print("Cloning {0}".format(repo))
        Git(archive_path).clone(repo.url.replace("https://","git://"))
        #Add option for different backend like S3
        #Add some error handling
        payload = {'archived':True}
        r = requests.patch("http://127.0.0.1:8000/api/repo/{0}/".format(repo.node), data=payload)
        #Add error handling
        print(r.status_code)

@periodic_task(run_every=(crontab(hour="*", minute="*")), name="search_repos_every_minute", ignore_result=True)
def github_repo_search():
	"""
	This searches Github for repos and then POSTs the repos back to the server.
	"""
	now = datetime.now()
	print(now.strftime('%Y-%m-%dT%H:%M:%S%z'))
	time_threshold = now - timedelta(seconds=60)
	#print(time_threshold.strftime('%Y-%m-%dT%H:%M:%S%z'))
	query = models.Query.objects.filter(last_searched__lt=time_threshold)
	if len(query) == 0:
		query = models.Query.objects.filter(last_searched=None)[0]
		print(query)
	if len(query) > 0:
		query_string = query.string
		lang_string = query.language
		if lang_string:
			search_param = "?q={0}+language:{1}&sort=updated&per_page=100&".format(query_string, lang_string)
		else:
			search_param = "?q={0}&sort=updated&per_page=100".format(query_string)
		print(github_search_url + search_param)
		r = requests.get(github_search_url + search_param)
		if r.status_code == requests.codes.ok:
			utc = pytz.utc
			last_searched = datetime.now(tz=utc)
			payload = {"last_searched":last_searched}
			last_search = requests.patch("http://127.0.0.1:8000/api/query/{0}/".format(query.id), data=payload)
			print("Found {0} Repos".format(len(r.json()['items'])))
			for idx, i in enumerate(r.json()['items']):
				print(idx)
				try:
					utc = pytz.utc
					last_checked = datetime.now(tz=utc)
					#There might be a way to have celery worker return this info instead of POSTing to API
					payload = {"url":i['html_url'], "node":i['node_id'], "create_date":i['created_at'], "description":i['description'], "last_checked":last_checked}
					bombs_away = requests.post("http://127.0.0.1:8000/api/repo/", data=payload)
				except:
					print("[ERROR] Failed to process: {0}".format(i['html_url']))
