from django.contrib import admin
from django import forms

from .models import Analysis, AnalysisDataset, AnalysisTag, AnalysisStep


admin.site.register(Analysis)
admin.site.register(AnalysisTag)
admin.site.register(AnalysisDataset)
admin.site.register(AnalysisStep)



