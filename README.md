![image](https://user-images.githubusercontent.com/46699116/79952710-abddf180-842f-11ea-90ef-425533be91bf.png)

# GitRecycle

This is a project to test the idea of creating a recycle bin for public github repos in order to find ones that are either deleted or went from public to private in a timeframe, such as in the case of an accident or forced removal. This is the original idea, it may flux a bit.

# How it works

Keywords are added and workers search Github at interval for new repos. Those repos are archived.

A time limit is set. If the repo goes missing within that time, an alert is generated to review it.

The alerted repo can be dismissed or saved. If dismissed, the archived copy of the repo is deleted.

If the time limit expires, and the repo has not gone missing, the repo is considered to be stale and is deleted from storage.

# Why?

I once accidentally set a private repo to public and know others that have too. Github also chooses it as the default repo type when creating a new repo. A repo that Github chooses or is forced to take down will appear to go missing the same as if it went private. I recently thought about what data you might find with certain keywords if you started scraping repos and saving/alerting to ones that vanish within a (short) period of time. How much private data is being exposed that shouldn't have been. During initial testing, in the course of a few hours, searching one keyword, I captured 3 projects that went to private or were deleted. Two of those were just college projects, but did not come back as public repos either. The 3rd was an AI researchers project.

# Stack

This is in early development, so everything is configured to defaults for development and no auth.

* Python
* Redis
* Celery
* Django
* DRF
* React

# Usage

## General steps
1. Start a redis docker instance
1. Set up the DRF project
1. Create a superuser 
1. Specifiy the repo storage path (I am using a NFS mount)
1. Start the DRF project
1. Create some fixture data in the Query model.
1. Start the celery worker (doing work and beat scheduling)
1. Start the react frontend

## Docker

This uses Redis for both the broker and the backend service at the moment. You can use the default docker image for development.

`docker pull redis`  
`docker run --name "GitRecycle-redis" -d -p 6379:6379 redis`  

## Virtual Environment

`virtualenv .venv`
`source .venv/bin/activate`

## PIP packages

`pip3 install -r requirements.txt`

## DRF

Enter the project directory

`cd GitRecycle`

Make the migrations and create the db

`python3 manage.py makemigrations Recycler && python3 manage.py migrate`

Create your superuser

`python3 manage.py createsuperuser --username scooty --email scooty@localhost`

Start it like any other django project

`python3 manage.py runserver 127.0.0.1:8000`

Without any Query data, the workers can't search Github for repos and generate work. Go to the admin at http://127.0.0.1/admin/ and log in as the superuser. Go to the Query objects and click the + button to create a new Query object.

## Environment Variables

* REPO_STORAGE_PATH - This is the path to where the repos will be saved

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

## React Frontend

There is a simple react frontend to render a list of repos.

![image](https://user-images.githubusercontent.com/46699116/80047048-3b7fb080-84c1-11ea-9adc-4390d086c036.png)

Install the dependencies

`npm install --save reactstrap react react-dom`

Start the project

`cd gitrecycle-frontend`  
`yarn start` or `npm start`  

If there are no errors, you can browse to the development server at http://127.0.0.1:3000

# Endpoints

Main endpoints are /api/repo/ and /api/query/

## Repo

*  /api/repo/ - Lists all repos
*  /api/repo/fresh/ - Lists repos that are still fresh and being checked
*  /api/repo/stale/ - Lists repos that have gone stale
*  /api/repo/archived/ - Lists repos that have been archived

## Query

*  /api/query/ - Lists the current strings to use as search queries
