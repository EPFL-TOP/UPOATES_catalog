from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
import os, json


#___________________________________________________________________________________________
class RawDataset(models.Model):
    """Model representing the raw dataset with a unique connection to a raw dataset on the RCP storage"""
    """Below are two list specific to the laboratory"""
    
    DATA_STATUS = (
        ('available',    'Available'),
        ('notavailable', 'Not available'),
        ('deleted',      'Deleted')
    )

    COMPRESSION_TYPE = (
        ('none', 'None'),
        ('jeraw', 'JetRaw'),
        ('zip','Zip'),
        ('tar','Tar'),
    )

    FILE_FORMAT = (
        ('none', 'None'),
        ('tiff', 'tiff'),
        ('nd2','nd2'),
        ('fastq','fastq'),
    )

    data_type       = models.CharField(max_length=100, help_text='Type of data for this dataset (reflecting the the RCP storage categories)')
    data_name       = models.CharField(max_length=100, help_text="Name of the experimental dataset folder on the RCP storage.")
    number_of_raw_files = models.CharField(max_length=10, help_text='Number of files for this dataset.', default='')
    total_raw_size      = models.CharField(max_length=100, help_text='Total size for this dataset (in bytes).', default='')
    number_of_other_files = models.CharField(max_length=10, help_text='Number of files for this dataset.', default='')
    total_other_size      = models.CharField(max_length=100, help_text='Total size for this dataset (in bytes).', default='')
    data_status     = models.CharField(max_length=100, choices=DATA_STATUS, default='', help_text='Status of the data on the RCP storage.')
    date_added      = models.DateField(null=True, help_text="Date automatically registered (when pushing the refresh button)")
    date_removed    = models.DateField(blank=True, null=True, help_text="Date when the rawdataset is removed from RCP")
    raw_files       = models.JSONField(null=True)
    other_files     = models.JSONField(null=True)
    compression     = models.CharField(blank=True, max_length=100, choices=COMPRESSION_TYPE, default='', help_text='Type of compression if any')
    file_format     = models.CharField(blank=True, max_length=100, choices=FILE_FORMAT, default='', help_text='Format of the files')

    #experimental_sample = models.ManyToManyField(ExperimentalSample, blank=True,help_text="Select experimental samples for this experimental dataset", default='', null=True)



    def get_absolute_url(self):
        """Returns the url to access a particular contributor instance."""
        return reverse('rawdataset-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the RawDataset object."""
        #return ''
        return '{0}, {1}, {2}, {3}, {4}'.format(self.data_type, self.data_name, self.data_status, self.number_of_files, self.total_size)


    class Meta:
        ordering = ('data_type','data_name',)