from django.contrib import admin
from django import forms

# Register your models here.

from .models import Contribution, ContributionOrigin, ContributionType, Contributor, Affiliation, Person


admin.site.register(Contribution)
admin.site.register(ContributionOrigin)
admin.site.register(ContributionType)
admin.site.register(Contributor)
admin.site.register(Person)
admin.site.register(Affiliation)