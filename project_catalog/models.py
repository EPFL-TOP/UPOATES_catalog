from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
from experiment_catalog.models import ExperimentalDataset
from contribution_catalog.models import Contribution
# Create your models here.

#___________________________________________________________________________________________
class ProjectTag(models.Model):
    """Model representing an experimental tag"""
    name        = models.CharField(max_length=200, help_text="Short name for the project tag")
    description = models.TextField(blank=True,max_length=2000, help_text="Enter a brief description of the project tag")

    class Meta:
        verbose_name = 'Project tag'
        verbose_name_plural = 'Project tags'
        ordering = ["name"]


    def get_absolute_url(self):
        """Returns the url to access a particular experimental tag instance."""
        return reverse('projecttag-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return  self.name
    
#___________________________________________________________________________________________
class Zenodo(models.Model):
    """Model representing a publication"""
    title  = models.CharField(max_length=200, help_text="Title for the zenodo entry")
    doi    = models.CharField(max_length=40, help_text="Provide the zenodo DOI in the form: 10.5281/zenodo.8211680")
  
    def get_absolute_url(self):
        """Returns the url to access a particular zenodo instance."""
        return reverse('zenodo-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}, {1}'.format(self.doi, self.title)

#___________________________________________________________________________________________
class Publication(models.Model):
    """Model representing a publication"""
    name_short      = models.CharField(max_length=200, help_text="Short name for the publication")
    bioarxiv_id     = models.CharField(max_length=200, help_text="Bioarxiv id for the publication using a specific experiment in the form e.g.: 2023.08.02.551629v2")
    bioarxiv_title  = models.CharField(max_length=200, help_text="Bioarxiv title for the publication using a specific experiment")
    journal_id      = models.CharField(blank=True, max_length=200, help_text="Journal id for the publication using a specific experiment")
    journal_title   = models.CharField(blank=True, max_length=200, help_text="Journal title for the publication using a specific experiment")
  
    def get_absolute_url(self):
        """Returns the url to access a particular publication instance."""
        return reverse('publication-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}, {1}, {2}'.format(self.name_short, self.bioarxiv_id, self.bioarxiv_title)


#___________________________________________________________________________________________
class Project(models.Model):
    """Model representing a project"""
    PROJ_STATUS = (
        ('ongoing','Ongoing'),          #data analysis ongoing
        ('published','Published'),      #data analysis finished and published
        ('paused','Paused'),            #data analysis paused
        ('finished','Finished'),        #data analysis finished and un-published
        ('terminated', 'Terminated')    #data analysis terminated, and not published will no longer use the data
    )

    name         = models.CharField(default="", max_length=200, help_text="Name of the project")
    start_date   = models.DateField(null=True, help_text="Start date of the project in format: MM/DD/YYYY")
    status       = models.CharField(max_length=20, choices=PROJ_STATUS, default='Ongoing', help_text='Status of the project')
    dataset      = models.ManyToManyField(ExperimentalDataset, help_text="Choose one or several experiment(s) for this project", related_name="project_dataset")
    project_tag  = models.ManyToManyField(ProjectTag, help_text="Select project tag(s) for this project")
    description  = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the project")
    publication  = models.ManyToManyField(Publication, blank=True, help_text="Select publication(s) for this project")
    zenodo       = models.ManyToManyField(Zenodo, blank=True, help_text="Select zenodo(s) for this project")
    contribution = models.ManyToManyField(Contribution, blank=True, help_text="Contribution(s) for this project")
    end_date     = models.DateField(blank=True, null=True, help_text="End date of the project in format: MM/DD/YYYY")

    def get_absolute_url(self):
        """Returns the url to access a particular treatment instance."""
        return reverse('project-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the project object"""
        return '{0}, {1}, {2}'.format(self.start_date, self.name, self.status)

    class Meta:
        ordering = ("start_date", "name")

