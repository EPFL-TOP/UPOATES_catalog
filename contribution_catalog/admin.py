from django.contrib import admin
from django import forms

# Register your models here.

from .models import Contribution, Contributor, Affiliation, Person

class PersonAdmin(admin.ModelAdmin):
    search_fields = [ "first_name", "last_name"]

admin.site.register(Contribution)
admin.site.register(Contributor)
admin.site.register(Person, PersonAdmin)
admin.site.register(Affiliation)