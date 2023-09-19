from django.contrib import admin
from django import forms

# Register your models here.
from .models import ExperimentalDataset, Experiment, ExperimentalTag


class ExperimentalDatasetAdmin(admin.ModelAdmin):
    #list_display = ('title', 'description', 'author', 'year')
    search_fields = ["raw_dataset__data_type","raw_dataset__data_name"]

admin.site.register(ExperimentalDataset, ExperimentalDatasetAdmin)
admin.site.register(Experiment)
admin.site.register(ExperimentalTag)
