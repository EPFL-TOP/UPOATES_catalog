from django.contrib import admin
from django import forms

# Register your models here.
from .models import Project, Publication, ProjectTag, Zenodo

admin.site.register(Project)
admin.site.register(Publication)
admin.site.register(ProjectTag)
admin.site.register(Zenodo)
