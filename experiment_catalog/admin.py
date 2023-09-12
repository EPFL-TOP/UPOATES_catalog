from django.contrib import admin
from django import forms

# Register your models here.
from .models import ExperimentalDataset

admin.site.register(ExperimentalDataset)
