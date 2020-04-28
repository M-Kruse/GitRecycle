from django.urls import reverse
from django.shortcuts import get_object_or_404

from git import Git, Repo
from git.exc import InvalidGitRepositoryError

from celery import task, shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from Recycler import models

import requests
from datetime import datetime, timedelta, timezone
import pytz
import os

import shutil

repo_storage_path = os.environ['REPO_STORAGE_PATH']

github_search_url = "https://api.github.com/search/repositories"

logger = get_task_logger(__name__)

@shared_task()
def clone_repo(repo_pk):
    try:
        repo = models.Repo.objects.get(pk=repo_pk, archived=False)
        print(repo)
    except models.Repo.DoesNotExist:
        repo = None
    if repo:
        print("Cloning {0}".format(repo))
        Git(repo_storage_path).clone(repo.url.replace("https://","git://"))
        #Add option for different backend like S3
        #Add some error handling
        repo.archive_path = repo_storage_path + repo.url.split("/")[-1]
        repo.save()

@periodic_task(run_every=(crontab(hour="*", minute="*")), name="search_repos_every_minute", ignore_result=True)
def github_repo_search():
    """
    This searches Github for repos and then POSTs the repos back to the server.
    """
    now = datetime.now()
    print(now.strftime('%Y-%m-%dT%H:%M:%S%z'))
    time_threshold = now - timedelta(seconds=60)
    #print(time_threshold.strftime('%Y-%m-%dT%H:%M:%S%z'))
    queryset = models.Query.objects.filter(last_searched=None)
    if queryset.count() == 0:
        queryset = models.Query.objects.filter(last_searched__lt=time_threshold)
    if queryset.count() > 0:
        query = queryset[0]
        print(query)
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
            last_search = requests.patch("http://127.0.0.1:8000/api/query/{0}/".format(query.id), data=payload, headers={'Authorization': 'Token {0}'.format(auth_token)})
            print("Found {0} Repos".format(len(r.json()['items'])))
            for idx, i in enumerate(r.json()['items']):
                print(idx)
                try:
                    utc = pytz.utc
                    last_checked = datetime.now(tz=utc)
                    new_repo = models.Repo(node=i['node_id'], url=i['html_url'], create_date=i['created_at'], description=i['description'], last_checked=last_checked)
                    #Add error handling here
                    new_repo.save()
                except Exception as e:
                    print("[ERROR] Failed to process: {0} | ERROR: {1}".format(i['html_url'], e))

@periodic_task(run_every=3, name="test_if_repo_public_every_3_second", ignore_result=True)
def is_repo_public():
    """
    Test if the repo still is public or inaccessible, report back to the server the result
    """
    now = datetime.now()
    print(now.strftime('%Y-%m-%dT%H:%M:%S%z'))
    time_threshold = now - timedelta(seconds=60)
    #print(time_threshold.strftime('%Y-%m-%dT%H:%M:%S%z'))
    queryset = models.Repo.objects.filter(last_checked=None)
    if queryset.count() == 0:
        queryset = models.Repo.objects.filter(last_checked__lt=time_threshold).order_by('last_checked')
    if queryset.count() > 0:
        repo = queryset[0]
        repo_url = repo.url
        repo_node = repo.node
        print("[INFO] Checking public repo: {0}".format(repo_url))
        r = requests.get(repo_url)
        if r.status_code == requests.codes.ok:
            utc = pytz.utc
            last_checked = datetime.now(tz=utc)
            repo.last_checked = last_checked
            repo.save()
            print("[INFO] Repo is still public: {0}".format(repo_url))
        #If we do too many requests and hit a rate limit, we can get 429 response
        elif r.status_code == 429:
            err = "[ERROR] Triggered Status Code 429 - Too Many Requests "
            print(err)
        #We assume this means that the repo has gone missing. The server will check it as well for sanity.
        elif r.status_code == 404:
            print("[INFO] DETECTED MISSING REPO!!")
            utc = pytz.utc
            last_checked = datetime.now(tz=utc)
            #We send a Patch with a bool to indicate it went missing
            payload = {'last_checked':last_checked, 'missing':True}
            repo.missing = True
            repo.last_checked = last_checked
            repo.save()
        else:
            err = "[ERROR] Unknown Errror - {0}".format(r.status_code)
            print(err)
    else:
        print("[INFO] Failed to find repo to test...")

@periodic_task(run_every=300, name="check_stale_repos_every_5_minute", ignore_result=True)
def is_repo_stale():
    """
    Test if the repo has gone stale, past the expire time for it to be considered interesting anymore.
    """
    # scrape_date - deltatime()
    try:
        queryset = models.Repo.objects.filter(archived=True)
    except models.Repo.DoesNotExist:
        queryset = None
    if queryset:
        if queryset.count() > 0:
            for repo in queryset:
                stale_time = repo.scrape_date + timedelta(minutes=1) #Stale time
                if datetime.now(timezone.utc) >= stale_time:
                    repo.stale = True
                    repo.save()
                    print("[INFO] Repo has gone stale {0} ...".format(repo.url))


@periodic_task(run_every=900, name="remove_stale_repos_every_15_minute", ignore_result=True)
def remove_repo():
     try:
        queryset = models.Repo.objects.filter(archived=True, stale=True, missing=False)
     except models.Repo.DoesNotExist:
        queryset = None
     if queryset.count() > 0:
        repo = queryset.first()
        print("[INFO] Deleting Repo: {0}".format(repo.url))
        if repo.archive_loc:
            if os.path.isdir(repo.archive_loc):
                #Little sanity check to make sure the path is not totally bogus
                if repo_storage_path in repo.archive_loc:
                    print(shutil.rmtree(repo.archive_loc))
                    #Test if the repo was succesfully removed
                    models.Repo.objects.get(pk=repo.node).delete()
                    print("[INFO] Deleted Repo: {0}".format(repo.url))
            else:
                print("[ERROR] Could not validate archive location in order to delete: {0}".format(repo.archive_loc))


@periodic_task(run_every=60, name="get_storage_metrics_every_minute", ignore_result=True)
def get_storage_metrics():
    try:
        total_size = 0
        for path, dirs, files in os.walk(repo_storage_path):
            for f in files:
                fp = os.path.join(path,f)
                total_size += os.path.getsize(fp)
        print('Repo Storage Size: {:,} GB'.format(int(total_size/1024**3)).replace(',', ' '))
    except Exception as e:
        print(e)