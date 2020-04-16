from django.contrib import admin

from .models import Repo, Query, DeletedRepo

admin.site.register(Repo)
admin.site.register(Query)