![image](https://user-images.githubusercontent.com/46699116/79952710-abddf180-842f-11ea-90ef-425533be91bf.png)

# GitRecycle

This is a project to test the idea of creating a recycle bin for public github repos in order to find ones that are either deleted or went from public to private in a short timeframe, such as in the case of an accident or forced removal. This is the original idea, it may flux a bit.

# How it works

Keywords are added and workers search Github at interval for new repos. Those repos are archived.

A time limit is set. If the repo goes missing within that time, an alert is generated to review it.

The alerted repo can be dismissed or saved. If dismissed, the archived copy of the repo is deleted.

If the time limit expires, and the repo has not gone missing, the repo is considered to be stale and is deleted from storage.

# Add some example query data

Workers will call the API to get the keywords lists they are to search.

`python manage.py shell`

`for q in ['cve', 'malware', 'exploit', 'hack', 'bot', 'ransom', 'malicious', 'attack', 'deep', 'ml', 'machine learning', 'neural']: Query(string=q).save()`                                             


```
In [15]: Query.objects.all()                                                                                                                                                                                    
Out[15]: <QuerySet [<Query: cve>, <Query: malware>, <Query: exploit>, <Query: hack>, <Query: bot>, <Query: ransom>, <Query: malicious>, <Query: attack>, <Query: deep>, <Query: ml>, <Query: machine learning>, <Query: neural>]>
```

# Why?

I accidentally set a private repo to public in the past and know others that have too. This also happens when Github chooses or is forced to take down a repo. I recently thought what you might find with certain keywords if you started scraping new repos and saving/alerting to ones that vanish within a (short) period of time.

# Endpoints

Main endpoints are /api/repo/ and /api/query/

## Repo

*  /api/repo/ - Lists all repos
*  /api/repo/fresh/ - Lists repos that are still fresh and being checked
*  /api/repo/stale/ - Lists repos that have gone stale
*  /api/repo/archived/ - Lists repos that have been archived

## Query

*  /api/query/ - Lists the current strings to use as search queries

# Usage

## General steps
1. Start a redis docker instance
1. Set up the DRF project
1. Create a superuser 
1. Start the DRF project
1. Create some fixture data in the Query model.
1. Start the project and beat worker

## Docker

This uses Redis for both the broker and the backend service at the moment. You can use the default docker image for development.

`docker pull redis`
`docker run --name "GitRecycle-redis" -d -p 6379:6379 redis`

## DRF

Enter the project directory

`cd GitRecycle`

Make the migrations and create the db

`python3 manage.py makemigrations && python3 manage.py migrate`

Create your superuser

`python3 manage.py createsuperuser --username scooty --email scooty@localhost`

Start it like any other django project

`python3 manage.py runserver 127.0.0.1:8000`

Without any Query data, the workers can't search Github for repos and generate work. Go to the admin at http://127.0.0.1/admin/ and log in as the superuser. Go to the Query objects and click the + button to create a new Query object.

## Celery Worker

Currently Celery is hooked into the Repo model's post save function to send newly saved github repos to a celery worker queue which uses GitRecycle/tasks.py

### How to start workers

From the root DRF project directory, run the worker and the beat

`celery -A GitRecycle worker -l debug -B`

Currently the beat is scheduled like this
	
	* New repos are scheduled every minutes
	* Repo visibility is scheduled every second

You can also POST repo info to the API or use the admin console to manually add and test

The schedule needs to be played with more, tuned to avoid spammming with requests. ***Use at your own risk***
