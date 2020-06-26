import csv

from django.contrib import admin
from pclub import models
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import HomepageImages, Events, Teams, EventGallery, Resources, Tags, Sub_Tags,Newsletter


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('team',)


admin.site.register(Teams, TeamsAdmin)


class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('resource',)


admin.site.register(Resources, ResourcesAdmin)
admin.site.register(HomepageImages)
admin.site.register(Events)
admin.site.register(EventGallery)

admin.site.register(Tags)
admin.site.register(Sub_Tags)
admin.site.register(Newsletter)

