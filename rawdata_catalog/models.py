from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
import os, json



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
class ExperimentalTag(models.Model):
    """Model representing an experimental tag"""
    name_short  = models.CharField(max_length=200, help_text="Short name for the experimental tag")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name the experimental tag")
    description = models.TextField(blank=True,max_length=2000, help_text="Enter a brief description of the experimental tag")

    class Meta:
        verbose_name = 'Experimental tag'
        verbose_name_plural = 'Experimental tags'

    def get_absolute_url(self):
        """Returns the url to access a particular experimental tag instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short


#___________________________________________________________________________________________
class ProjectTag(models.Model):
    """Model representing an experimental tag"""
    name_short  = models.CharField(max_length=200, help_text="Short name for the project tag")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name the project tag")
    description = models.TextField(blank=True,max_length=2000, help_text="Enter a brief description of the project tag")

    class Meta:
        verbose_name = 'Project tag'
        verbose_name_plural = 'Project tags'

    def get_absolute_url(self):
        """Returns the url to access a particular experimental tag instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short


#___________________________________________________________________________________________
class Treatment(models.Model):
    """Model representing a treatment"""
    name_short  = models.CharField(max_length=200, help_text="Short name for treatment")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name for treatment")
    description = models.TextField(blank=True,max_length=2000, help_text="Enter a brief description of the treatment")

    def get_absolute_url(self):
        """Returns the url to access a particular treatment instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short


#___________________________________________________________________________________________
class Injection(models.Model):
    """Model representing a treatment"""
    name_short  = models.CharField(max_length=200, help_text="Short name for injection")
    name_long   = models.CharField(blank=True, max_length=200, help_text="Long name for injection")
    description = models.TextField(blank=True,max_length=2000, help_text="Enter a brief description of the injection")

    def get_absolute_url(self):
        """Returns the url to access a particular injection instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name_short

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
class ExperimentalContribution(models.Model):
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

#___________________________________________________________________________________________
class Experiment(models.Model):
    """Model representing an experiment."""  
    experiment_name   = models.CharField(max_length=100, help_text="Name of the experiment.")
    date              = models.DateField(null=True, help_text="date the experiment is done")
    experimental_tag  = models.ManyToManyField(ExperimentalTag, help_text="Select experimental tag(s) for this experiment")
    contribution      = models.ManyToManyField(ExperimentalContribution, blank=True, help_text="Select contribution(s) for this experiment")
    treatment         = models.ManyToManyField(Treatment, blank=True, help_text="Select treatment(s) for this experiment")
    injection         = models.ManyToManyField(Injection, blank=True, help_text="Select injection(s) for this experiment")
    description       = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the experiment")

    def get_absolute_url(self):
        """Returns the url to access a particular contributor instance."""
        return reverse('experiment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Contributor object."""
        return '{0}, {1}'.format(self.experiment_name, self.date)


#___________________________________________________________________________________________
class ExperimentalSample(models.Model):
    """Model representing the experimental sample of an experiment."""

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
    rcp_name        = models.CharField(max_length=100, help_text="Name of the experimental dataset folder on the RCP storage.")
    number_of_files = models.CharField(max_length=10, help_text='Number of files for this dataset.', default='')
    total_size      = models.CharField(max_length=100, help_text='Total size for this dataset (in bytes).', default='')
    data_status     = models.CharField(max_length=100, choices=DATA_STATUS, default='', help_text='Status of the data on the RCP storage.')
    date_added      = models.DateField(null=True, help_text="Date automatically registered (when pushing the refresh button)")
    files_data      = models.JSONField(null=True)
    compression     = models.CharField(blank=True, max_length=100, choices=COMPRESSION_TYPE, default='', help_text='Type of compression if any')
    file_format     = models.CharField(blank=True, max_length=100, choices=FILE_FORMAT, default='', help_text='Format of the files')

    #experimental_sample = models.ManyToManyField(ExperimentalSample, blank=True,help_text="Select experimental samples for this experimental dataset", default='', null=True)



    def get_absolute_url(self):
        """Returns the url to access a particular contributor instance."""
        return reverse('rawdataset-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the RawDataset object."""
        #return ''
        return '{0}, {1}, {2}, {3}, {4}'.format(self.data_type, self.rcp_name, self.data_status, self.number_of_files, self.total_size)


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
    date         = models.DateField(null=True, help_text="Date field in format: MM/DD/YYYY")
    status       = models.CharField(max_length=20, choices=PROJ_STATUS, default='Ongoing', help_text='Status of the project')
    experiment   = models.ManyToManyField(Experiment, blank=True, help_text="Choose one or several experiment(s) for this project")
    description  = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the project")
    publication  = models.ManyToManyField(Publication, blank=True, help_text="Select publication(s) for this project")
    zenodo       = models.ManyToManyField(Zenodo, blank=True, help_text="Select zenodo(s) for this project")
    project_tag  = models.ManyToManyField(ProjectTag, help_text="Select project tag(s) for this experiment")

    def get_absolute_url(self):
        """Returns the url to access a particular treatment instance."""
        return reverse('project-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the project object"""
        return '{0}, {1}'.format(self.name, self.date)



class Blog(models.Model):
    NAMES = (
        ('name1','name1'),
        ('name2','name2'),
        ('name3','name3'),
        ('name4','name4'), 
        ('name5','name5'),
    )

    SUBNAMES = (
        ('subname1','subname1'),
        ('subname2','subname2'),
        ('subname3','subname3'),
        ('subname4','subname4'), 
        ('subname5','subname5'),
    )

    name     = models.CharField(max_length=100, choices=NAMES)
    sub_name = models.CharField(max_length=100, choices=SUBNAMES, default='')

    def __str__(self):
        return self.name+' '+self.sub_name



#{"common": { "authors": [],                -> DONE 
#            "laboratory_contributors": [], -> DONE
#            "external_contributors": [],   -> DONE
#            "experiment_name": "",         -> DONE
#            "starting_date":               -> DONE
#            "status": [],                  -> DONE 
#            "experimental_tags": [],       -> DONE
#            "bioarxiv_tags": [],           -> DONE
#            "journal_tags": [],            -> DONE
#            "zenodo_tags": []              -> DONE
        # "fish_lines": [], "mutations": [], "phenotypes": [], "slim_ids": [], "pyrat_ids": [], }, "specific": {"coating": [], "treatment": [], "npositions": ""}}

