from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
from django.core.exceptions import ObjectDoesNotExist

DEV_STAGE = (
    ('2cells','2 Cells'),
    ('4cells','4 Cells'),
    ('8cells','8 Cells'),
    
    ('12somites',    '12 Somites'),
    )


# Create your models here.

#___________________________________________________________________________________________
class ParentLine(models.Model):
    name_short  = models.CharField(max_length=200, help_text="Short name for the fish line")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name for fish line")
    description = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the fish line")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short


#___________________________________________________________________________________________
class Mutation(models.Model):
    name_short  = models.CharField(max_length=200, help_text="Short name for the fish line")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name for fish line")
    description = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the fish line")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short

#___________________________________________________________________________________________
class MutationGrade(models.Model):
    name_short  = models.CharField(max_length=200, help_text="Short name for the fish line")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name for fish line")
    description = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the fish line")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short

#___________________________________________________________________________________________
class Treatment(models.Model):
    """Model representing a treatment"""
    name_short          = models.CharField(max_length=200, help_text="Short name for treatment")
    developmental_stage = models.CharField(max_length=100, choices=DEV_STAGE, default='', help_text='Developmental stage')
    name_long           = models.CharField(blank=True, max_length=200, help_text="Long name for treatment")
    description         = models.TextField(blank=True,max_length=2000, help_text="Enter a brief description of the treatment")

    def get_absolute_url(self):
        """Returns the url to access a particular treatment instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return "{0}, {1}".format(self.name_short, self.developmental_stage)


#___________________________________________________________________________________________
class Injection(models.Model):
    """Model representing a treatment"""
    name_short  = models.CharField(max_length=200, help_text="Short name for injection")
    developmental_stage = models.CharField(max_length=100, choices=DEV_STAGE, default='', help_text='Developmental stage')
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name for injection")
    description = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the injection")

    def get_absolute_url(self):
        """Returns the url to access a particular injection instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return "{0}, {1}".format(self.name_short, self.developmental_stage)


#___________________________________________________________________________________________
class Animal(models.Model):
    """Model representing an experiment."""  
    SPECIE_TYPE = (
        ('zebrafish',    'Zebra fish'),
    )

    specie              = models.CharField(max_length=100, choices=SPECIE_TYPE, default='zebrafish', help_text='Type of animal(s) used for this experimental dataset.')
    developmental_stage = models.CharField(max_length=100, choices=DEV_STAGE, default='', help_text='Developmental stage')
    parent_line         = models.ManyToManyField(ParentLine, default='', help_text='Parents fish lines')
    mutation            = models.ManyToManyField(Mutation,  default='', help_text='mutation')
    mutation_grade      = models.ManyToManyField(MutationGrade,  default='', help_text='mutation grade')

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        parent_lines = "("+", ".join(str(par) for par in self.parent_line.all())+")"
        mutations =  "("+", ".join(str(par) for par in self.mutation.all())+")"
        mutation_grades =  "("+", ".join(str(par) for par in self.mutation_grade.all())+")"
        return '{0}, {1}, {2}, {3}, {4} '.format(self.specie, self.developmental_stage, parent_lines, mutations, mutation_grades)

    class Meta:
        ordering = ["specie", "developmental_stage"]


#___________________________________________________________________________________________
class ExperimentalCondition(models.Model):
    """Model representing the experimental dataset of a given raw-dataset."""  

    animal     = models.ManyToManyField(Animal, help_text="Species used")
    treatment  = models.ManyToManyField(Treatment, blank=True, help_text="Treatment(s) for this experimental dataset.")
    injection  = models.ManyToManyField(Injection, blank=True, help_text="Injection(s) for this experimental dataset.")


    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        #ee=ExperimentalCondition()

 

        #print('---pppppppppp',self.experimentaldataset)
#        #authors = ExperimentalCondition.objects
#        print()
        #ee=ExperimentalCondition()
#        #return ee.experimentaldataset
        try:
            return '{0}, {1}'.format(self.experimentaldataset.raw_dataset.data_type, self.experimentaldataset.raw_dataset.data_name)
        except ObjectDoesNotExist:
            return 'none'