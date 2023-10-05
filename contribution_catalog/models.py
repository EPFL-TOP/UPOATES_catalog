from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
 

# Create your models here.
#___________________________________________________________________________________________
class Affiliation(models.Model):
    """Model representing the affiliation"""
    short_name = models.CharField(max_length=200, help_text="Short name for the affiliation")
    long_name  = models.CharField(max_length=200, help_text="Long name for the affiliation")
    country    = models.CharField(max_length=200, help_text="Country of the of affiliation")
    department = models.CharField(max_length=200, help_text="Department name of the affiliation", blank=True, default="")
    institute  = models.CharField(max_length=200, help_text="Name of the institute for the affiliation", blank=True)
    laboratory = models.CharField(max_length=200, help_text="Name of the laboratory for the affiliation", blank=True)
    laboratory_internal = models.CharField(max_length=200, help_text="Internal name of the laboratory for the affiliation", blank=True)
 
    class Meta:
        ordering = ['short_name', 'laboratory']

    def get_absolute_url(self):
        """Returns the url to access a particular affiliation instance."""
        return reverse('affiliation-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Affiliation object"""
        toret='{0}, {1}'.format(self.short_name, self.long_name)
        if self.department!='':toret+=', '+self.department
        if self.institute !='':toret+=', '+self.institute
        if self.laboratory!='':toret+=', '+self.laboratory
        if self.laboratory_internal!='':toret+=', '+self.laboratory_internal
        toret+=', '+self.country
        return toret

#___________________________________________________________________________________________
class Person(models.Model):
    """Model representing a person."""
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    orcid       = models.CharField(blank=True, default="",max_length=19,help_text="Provide 16 digits orcid in the form: 0000-0000-0000-0000")
  
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular person instance."""
        return reverse('person-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Person object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)
                                                
    class Meta:
        ordering = ("first_name", "last_name")

#___________________________________________________________________________________________
class Contributor(models.Model):
    """Model representing a contributor."""
    person        = models.ForeignKey('Person', help_text="Select one person", on_delete=models.CASCADE)
    email_address = models.EmailField(default="")
    affiliation   = models.ManyToManyField(Affiliation, help_text="Select one or several affiliation for this contributor")

    def get_absolute_url(self):
        """Returns the url to access a particular contributor instance."""
        return reverse('contributor-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Contributor object."""
        affiliation=""
        if len(self.affiliation.values())>0: affiliation = self.affiliation.values()[0]["short_name"]
        for x in range(1,len(self.affiliation.values())): affiliation+=', '+self.affiliation.values()[x]["short_name"]

        #type=""
        #if len(self.type.values())>0: type = self.type.values()[0]["type"]
        #for x in range(1,len(self.type.values())): type+=', '+self.type.values()[x]["type"]

        #origin=""
        #if len(self.origin.values())>0: origin = self.origin.values()[0]["origin"]
        #for x in range(1,len(self.origin.values())): origin+=', '+self.origin.values()[x]["origin"]

        return '{0}, {1}, ({2})'.format(self.person, self.email_address, affiliation)


#___________________________________________________________________________________________
class ContributionType(models.Model):
    """Model representing a type contribution"""
    type  = models.CharField(max_length=200, help_text="Type of contribution")

    class Meta:
        verbose_name = 'Type of contribution'
        verbose_name_plural = 'Type of contributions'

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.type

#___________________________________________________________________________________________
class ContributionOrigin(models.Model):
    """Model representing the origin of a contribution"""
    origin  = models.CharField(max_length=200, help_text="Origin of the contribution")

    class Meta:
        verbose_name = 'Origin of the contribution'
        verbose_name_plural = 'Origin of the contributions'

    def __str__(self):
        """String for representing the Origin object"""
        return self.origin
    
    #___________________________________________________________________________________________
class Contribution(models.Model):
    """Model representing an experimental contribution."""
    contributor   = models.ManyToManyField(Contributor, help_text="Select a contributor")
    type          = models.ManyToManyField(ContributionType,   help_text="Select one or several type of contribution for this contributor")
    origin        = models.ManyToManyField(ContributionOrigin, help_text="Select one or several origin of contribution for this contributor")
    description   = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the contribution for this contributor")

    def get_absolute_url(self):
        """Returns the url to access a particular contributor instance."""
        return reverse('experimentalcontribution-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Contributor object."""
       
        #TODO, Trying to get the experiment and project from reverse m2m
        #contribution = Contribution.objects.get(id=4)
        #experiment = contribution.experiments.all()
        #print('--------------------experiment ',experiment)
        #Article.objects.filter(publications__title__startswith="Science")

        contributor = ""
        if len(self.contributor.all())>0: contributor=str(self.contributor.all()[0])
        for x in range(1,len(self.contributor.all())): contributor+="; "+str(self.contributor.all()[x])

        type = ""
        if len(self.type.values())>0: type = self.type.values()[0]["type"]
        for x in range(1,len(self.type.values())): type+=', '+self.type.values()[x]["type"]

        origin = ""
        if len(self.origin.values())>0: origin = self.origin.values()[0]["origin"]
        for x in range(1,len(self.origin.values())): origin+=', '+self.origin.values()[x]["origin"]

        return '{0}, ({1}), ({2})'.format(contributor, type, origin)
