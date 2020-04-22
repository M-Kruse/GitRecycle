![image](https://user-images.githubusercontent.com/46699116/79950662-40465500-842c-11ea-8c1f-c5e58c861dd2.png)

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

# Worker

Currently the Repo model has a hook in the post save function to send newly saved github URLs to a celery worker queue which uses GitRecycle/tasks.py

## How to start worker

From the root project directory, run the worker and the beat

`celery -A GitRecycle worker -l debug -B`

Currently the beat is scheduled like this
	
	* New repos are scheduled every minutes
	* Repo visibility is scheduled every second

You can also POST repo info to the API or use the admin console to manually add and test

