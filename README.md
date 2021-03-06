![image](https://user-images.githubusercontent.com/46699116/79952710-abddf180-842f-11ea-90ef-425533be91bf.png)

# GitRecycle aka "Git Dumpster Diver"

This is a project to test the idea of creating a recycle bin for public github repos in order to find ones that are either deleted or went from public to private in a timeframe, such as in the case of an accident or forced removal. This is the original idea, it may flux a bit.

# How it works

Keywords are added and workers search Github at interval for new repos. Those repos are archived.

A time limit is set. If the repo goes missing within that time, an alert is generated to review it.

The alerted repo can be dismissed or saved. If dismissed, the archived copy of the repo is deleted.

If the time limit expires, and the repo has not gone missing, the repo is considered to be stale and is deleted from storage.

# Why?

I once accidentally set a private repo to public and know others that have too. Github chooses it as the default repo type when creating a new repo. A repo that Github chooses or is forced to take down will appear to go missing the same as if it went private. I recently thought about what data you might find with certain keywords if you started scraping repos and saving/alerting to ones that vanish within a (short) period of time. How much private data is being exposed that shouldn't have been. See the [wiki](https://github.com/M-Kruse/GitRecycle/wiki/Scratch) for some example recycled repos during development testing. 

# Stack

This is in early development, so everything is configured to defaults for local development.

* Docker
* Python
* Redis
* Celery
* Django
* DRF
* React

# Usage

## General steps

1. Build with docker-compose
1. Init the database
1. Create a django superuser
1. Create an Auth token for the React frontend.
1. Create the .env_files for backend and frontend
1. Bring the containers up with docker-compose
1. Log in to the Django admin panel
1. Add Query model data

Build the docker images

`docker-compose build` 

Initalize the tables

`docker-compose run backend python3 manage.py makemigrations Recycler`  
`docker-compose run backend python3 manage.py migrate`  

Create your superuser

`docker-compose run backend python3 manage.py createsuperuser`

Request auth token for the user you just created

`docker-compose run backend python3 manage.py drf_create_token scooty`

Create your frontend env_file ( Replace YOUR_AUTH_TOKEN_GOES_HERE with the token generated in the last step)

`echo "REACT_APP_GITRECYCLE_AUTH_TOKEN=YOUR_AUTH_TOKEN_GOES_HERE" > gitrecycle-frontend/.env_file`

Create the backend env_file for repo archive storage location. This docker-compose.yml file maps ./Archive/ to /app/archive/ so the container onyl sees /app/archive/. *If you want to change it, change the mapping in the docker-compose.yml config.*

`echo "REPO_STORAGE_PATH=/app/archive/" > GitRecycle/.env_file`

Bring the containers up with docker-compose

`docker-compose up`

Open a browser, go to http://127.0.0.1:8000/admin and log in with your superuser.

Find the Query model in the list, click the +Add button, add a string to the field and click Save.

The workers should start to get query data on their next beat schedule and the react UI should be able to get data from the API. You can sanity check it by going to the Queries react page and checking if the Query you added is in the table.

## Celery Worker

Currently Celery is hooked into the Repo model's post save function to send newly saved github repos to a celery worker queue which uses GitRecycle/tasks.py

## React Frontend

There is a simple react frontend to render a list of repos at http://127.0.0.1:3000

![image](https://user-images.githubusercontent.com/46699116/80853111-e93a4000-8be2-11ea-90b6-31ec94793a4c.png)

![image](https://user-images.githubusercontent.com/46699116/80853153-33232600-8be3-11ea-8e7a-c6179aee5541.png)

![image](https://user-images.githubusercontent.com/46699116/80853106-e0e20500-8be2-11ea-9ebd-7a7a536ce839.png)

# Endpoints

## Repo

*  /api/repo/ - Lists all repos
*  /api/repo/missing/ - Lists repo that have been detec
*  /api/repo/fresh/ - Lists repos that are still fresh and being checked
*  /api/repo/stale/ - Lists repos that have gone stale

## Query

*  /api/query/ - Lists the current strings to use as search queries
