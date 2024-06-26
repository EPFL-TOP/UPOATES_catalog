from django.contrib import admin
from django import forms

# Register your models here.
from .models import Parent, Treatment, Injection, Sample, ExperimentalCondition, MutationGrade, MutationName, Mutation, InstrumentalCondition, Fixation, Marker


class ExperimentalConditionAdmin(admin.ModelAdmin):
    #list_display = ('title', 'description', 'author', 'year')
    search_fields = ["experimentaldataset__raw_dataset__data_type","experimentaldataset__raw_dataset__data_name"]
    #autocomplete_fields  = ["experimentaldataset__raw_dataset__data_type","experimentaldataset__raw_dataset__data_name"]
    
class SampleAdmin(admin.ModelAdmin):
    search_fields = ["experimentalcondition__experimentaldataset__raw_dataset__data_name"]
#        expds =  ", ".join("("+str(par.experimentaldataset.raw_dataset.data_name)+")" for par in self.experimentalcondition_set.all())


admin.site.register(Parent)
admin.site.register(Mutation)
admin.site.register(MutationGrade)
admin.site.register(MutationName)
admin.site.register(Treatment)
admin.site.register(Injection)
admin.site.register(Sample, SampleAdmin)
admin.site.register(ExperimentalCondition, ExperimentalConditionAdmin)
admin.site.register(InstrumentalCondition)
admin.site.register(Fixation)
admin.site.register(Marker)




