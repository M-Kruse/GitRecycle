from django.urls import reverse

from git import Git, Repo
from git.exc import InvalidGitRepositoryError

from Recycler import models
#from celeryboi import app

import requests

from celery import shared_task

archive_path = "/mnt/Personal/ApplicationData/GitRecycle/archives/"

@shared_task()
def clone_repo(pk):
        print("CELERY.tasks: Starting Task...")
        repo = models.Repo.objects.get(pk=pk)
        print(repo.url)
        print(repo.node)
        Git(archive_path).clone(repo.url.replace("https://","git://"))
        #Add option for different backend like S3
        #Add some error handling
        payload = {'archived':True}
        r = requests.patch("http://127.0.0.1:8000/api/repo/{0}/".format(repo.node), data=payload)
        print(r.status_code)