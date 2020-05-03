![image](https://user-images.githubusercontent.com/46699116/79952710-abddf180-842f-11ea-90ef-425533be91bf.png)

# GitRecycle

This is a project to test the idea of creating a recycle bin for public github repos in order to find ones that are either deleted or went from public to private in a timeframe, such as in the case of an accident or forced removal. This is the original idea, it may flux a bit.

# How it works

Keywords are added and workers search Github at interval for new repos. Those repos are archived.

A time limit is set. If the repo goes missing within that time, an alert is generated to review it.

The alerted repo can be dismissed or saved. If dismissed, the archived copy of the repo is deleted.

If the time limit expires, and the repo has not gone missing, the repo is considered to be stale and is deleted from storage.

# Why?

I once accidentally set a private repo to public and know others that have too. Github chooses it as the default repo type when creating a new repo. A repo that Github chooses or is forced to take down will appear to go missing the same as if it went private. I recently thought about what data you might find with certain keywords if you started scraping repos and saving/alerting to ones that vanish within a (short) period of time. How much private data is being exposed that shouldn't have been. See the wiki for some example recycled repos during development testing. 

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

1. Configure the env variables file
1. Build with docker-compose
1. Connect to the backend docker and start bash shell
1. Create a django superuser
1. Log in to the Django admin panel
1. Add Query model data
1. Create an Auth token for the React frontend.
1. Add the Auth token as a new env variable in the frontend docker container

Build the docker images

`docker-compose build` 

Initalize the tables

`docker-compose run backend python3 manage.py makemigrations Recycler`
`docker-compose run backend python3 manage.py mirgate`

You will need to create a superuser. Open up another terminal and run the createsuperuser command on the backend container

`docker-compose run backend python3 manage.py createsuperuser`

You also need an API Auth token for the frontend. Run the `drf_create_token` command on the backend container. The superuser I created in the previous step is named 'scooty' for this example.

`docker-compose run backend python3 manage.py drf_create_token scooty`

Take that generated token and create your .env_file in the gitrecycle-frontend folder

`echo "REACT_APP_GITRECYCLE_AUTH_TOKEN=YOUR_AUTH_TOKEN_GOES_HERE" > gitrecycle-frontend/.env_file`

Set the location to store the repos in your backend .env_file. This docker-compose.yml file maps ./Archive/ to /app/archive/ so the container onyl sees /app/archive/. *If you want to change it, change the mapping in the docker-compose.yml config.*

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

![image](https://user-images.githubusercontent.com/46699116/80047048-3b7fb080-84c1-11ea-9adc-4390d086c036.png)

# Endpoints

## Repo

*  /api/repo/ - Lists all repos
*  /api/repo/missing/ - Lists repo that have been detec
*  /api/repo/fresh/ - Lists repos that are still fresh and being checked
*  /api/repo/stale/ - Lists repos that have gone stale

## Query

*  /api/query/ - Lists the current strings to use as search queries
