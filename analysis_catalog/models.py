from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
import os, json

from project_catalog.models import Project

# Create your models here.

#___________________________________________________________________________________________
class AnalysisTag(models.Model):
    """Model representing an analysis tag"""
    name        = models.CharField(default='', max_length=200, help_text="Analysis tag name")
    description = models.TextField(blank=True, max_length=2000, help_text="Analysis tag description")

    class Meta:
        verbose_name = 'Analysis tag'
        verbose_name_plural = 'Analysis tags'
        ordering = ("name",)


    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name 


#___________________________________________________________________________________________
class Analysis(models.Model):
    """Model representing an analysis"""
    ANA_STATUS = (
        ('ongoing',  'Ongoing'),   #analysis ongoing
        ('paused',   'Paused'),    #analysis paused
        ('finished', 'Finished'),  #analysis finished
        ('stopped',  'Stopped')    #analysis stopped, for example found it's not optimal, and should create a new analysis
    )
    
    name         = models.CharField(max_length=100, help_text="Name of the analysis")
    status       = models.CharField(max_length=20, choices=ANA_STATUS, default='Ongoing', help_text='Status of the analysis')
    project      = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="Select one project for this analysis, if it does not exist, it needs to be created", related_name="analysis_project")
    description  = models.TextField(blank=True, max_length=2000, help_text="Description of the analysis")
    start_date   = models.DateField(null=True, help_text="Start date of the analysis in format: MM/DD/YYYY")
    end_date     = models.DateField(blank=True, null=True, help_text="End date of the analysis in format: MM/DD/YYYY")
    analysis_tag = models.ManyToManyField(AnalysisTag, help_text="Analysis tag(s) for this analysis")

    def __str__(self):
        """String for representing the Analysis object."""
        return '{0}, {1}, {2}'.format(self.name, self.start_date, self.status)
    
    class Meta:
        ordering = ("name","start_date")
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'

    def get_absolute_url(self):
        """Returns the url to access a particular analysis instance."""
        return reverse('analysis-detail', args=[str(self.id)])
    

#___________________________________________________________________________________________
class AnalysisDataset(models.Model):
    """Model representing an analysis dataset"""
    name  = models.CharField(max_length=100, help_text="Name of the analysis dataset")
    path  = models.CharField(max_length=200, help_text="Path of the analysis dataset inside upoates rcp share")

    files = models.JSONField(null=True, blank=True)
    number_of_files = models.CharField(blank=True, max_length=200, help_text="Path of the analysis dataset")
    total_size = models.CharField(blank=True, max_length=200, help_text="Path of the analysis dataset")


    def __str__(self):
        """String for representing the Analysis object."""
        return '{0}, {1}, {2}'.format(self.id, self.name, self.path)

    class Meta:
        ordering = ("-id",)

#___________________________________________________________________________________________
class AnalysisStep(models.Model):
    """Model representing an analysis step"""
    name           = models.CharField(max_length=100, help_text="Name of the analysis step")
    description    = models.TextField(blank=True, max_length=2000, help_text="Description of the analysis")
    step_number    = models.PositiveSmallIntegerField(default=0, help_text="Analysis step number")
    input_dataset  = models.ManyToManyField(AnalysisDataset, blank=True, help_text="Input dataset",  related_name="input_dataset")
    output_dataset = models.ManyToManyField(AnalysisDataset, blank=True, help_text="Output dataset", related_name="output_dataset")
    analysis       = models.ForeignKey(Analysis, default="", on_delete=models.CASCADE, related_name="analyses")


    def __str__(self):
        """String for representing the Analysis object."""
        return '{0}, {1}, {2}'.format(self.analysis.name, self.step_number, self.name)

    class Meta:
        ordering = ("analysis__name","step_number")