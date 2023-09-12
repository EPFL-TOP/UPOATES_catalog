from django.contrib import admin
from django import forms

# Register your models here.
from .models import ParentLine, Treatment, Injection, Animal, ExperimentalCondition, MutationGrade, Mutation

admin.site.register(ParentLine)
admin.site.register(Mutation)
admin.site.register(MutationGrade)
admin.site.register(Treatment)
admin.site.register(Injection)
admin.site.register(Animal)
admin.site.register(ExperimentalCondition)


