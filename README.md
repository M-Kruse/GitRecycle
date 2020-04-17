# GitRecycle

This is a project to test the idea of creating a recycle bin for public github projects in order to find projects that are either deleted or went from public to private in a short timeframe, such as in the case of an accident.

# How it works

Keywords are added and github is searched at interval for new repos. Those repos are archived.

A time limit is set. If the repo is deleted within that time, an alert is generated to review it.

The alerted repo can be dismissed or saved. If dismissed, the archived copy of the repo is deleted.

If the time limit expires, the repo is considered to be stale and is deleted from storage.

# Add some example query data

Workers will call the API to get the keywords lists they are to search.

`python manage.py shell`

`for q in ['cve', 'malware', 'exploit', 'hack', 'bot', 'ransom', 'malicious', 'attack', 'deep', 'ml', 'machine learning', 'neural']: Query(string=q).save()`                                             


```
In [15]: Query.objects.all()                                                                                                                                                                                    
Out[15]: <QuerySet [<Query: cve>, <Query: malware>, <Query: exploit>, <Query: hack>, <Query: bot>, <Query: ransom>, <Query: malicious>, <Query: attack>, <Query: deep>, <Query: ml>, <Query: machine learning>, <Query: neural>]>
```

# Why?

I accidentally set a private repo to public in the past and know others that have too. This also happens when Github chooses or is forced to take down a repo. I recently thought what you might find with certain keywords if you started scraping new repos and saving/alerting to ones that vanish within a (short) period of time, for whatever reason either deleted, set to private or removed by Github.

# Endpoints

Main endpoints are /api/repo/ and /api/query/ with /api/query/worker and /api/repo/worker serving the workers

## Repo

*  /api/repo/
*  /api/repo/fresh/
*  /api/repo/stale/
*  /api/repo/archived/
*  /api/repo/worker/

## Query

*  /api/query/
*  /api/query/worker/

# Worker

The current worker is using celery and at https://github.com/M-Kruse/GitRecycle-Worker