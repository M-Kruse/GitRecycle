from django.contrib import admin

from .models import Repo, Query, MissingRepo

admin.site.register(Repo)
admin.site.register(MissingRepo)
admin.site.register(Query)