from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms

from rawdata_catalog.models import RawDataset
from contribution_catalog.models import Contribution
from experimentalcondition_catalog.models import ExperimentalCondition
# Create your models here.

#___________________________________________________________________________________________
class ExperimentalTag(models.Model):
    """Model representing an experimental tag"""
    name        = models.CharField(default='', max_length=200, help_text="Experimental tag name")
    description = models.TextField(blank=True, max_length=2000, help_text="Experimental tag description")

    class Meta:
        verbose_name = 'Experimental tag'
        verbose_name_plural = 'Experimental tags'
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name 



#___________________________________________________________________________________________
class Experiment(models.Model):
    """Model representing an experiment."""  
    experiment_name   = models.CharField(max_length=100, help_text="Name of the experiment.")
    date              = models.DateField(null=True, help_text="Date of the experiment.")
    experimental_tag  = models.ManyToManyField(ExperimentalTag, help_text="Experimental tag(s) for this experiment")
    contribution      = models.ManyToManyField(Contribution, blank=True, help_text="Contribution(s) for this experiment")
    description       = models.TextField(blank=True, max_length=2000, help_text="Description of the experiment")

    def get_absolute_url(self):
        """Returns the url to access a particular Experiment instance."""
        return reverse('experiment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Experiment object."""
        return '{0}, {1}'.format(self.experiment_name, self.date)
    
    class Meta:
        ordering = ("experiment_name","date")

#___________________________________________________________________________________________
class ExperimentalDataset(models.Model):
    """Model representing the experimental dataset of a given raw-dataset."""  

    QUALITY = (

        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    )

    raw_dataset            = models.OneToOneField(RawDataset, on_delete=models.CASCADE, primary_key=True, help_text="Raw dataset for this experimental dataset.")
    experimental_condition = models.OneToOneField(ExperimentalCondition, on_delete=models.CASCADE, null=True, blank=True,   default='', help_text="Raw dataset for this experimental dataset.")
    experiment             = models.ForeignKey(Experiment, null=True, blank=True, on_delete=models.DO_NOTHING, default="")
    dataset_quality        = models.CharField(max_length=100, choices=QUALITY, default='', help_text='Dataset quality flag')
    def get_absolute_url(self):
        """Returns the url to access a particular Experiment instance."""
        return reverse('experimentaldataset-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Experiment object."""
        return '{0}, {1}'.format(self.raw_dataset.data_type, self.raw_dataset.data_name)
    
    class Meta:
        ordering = ("raw_dataset__data_type","raw_dataset__data_name")
