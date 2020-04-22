import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_publisher.settings')
 
app = Celery('Recycler',  backend='redis://localhost:6379', broker='redis://localhost:6379')

app.config_from_object('django.conf:settings')
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()