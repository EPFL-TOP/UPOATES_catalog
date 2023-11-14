from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Lower, Upper

DEV_STAGE = (
    ('1-cell (0.2h)',      '1-cell (0.2h)'),
    ('2-cells (0.75h)',    '2-cells (0.75h)'),
    ('4-cells (1h)',       '4-cells (1h)'),
    ('8-cells (1.25h)',    '8-cells (1.25h)'),
    ('16-cells (1.5h)',    '16-cells (1.5h)'),
    ('32-cells (1.75h)',   '32-cells (1.75h)'),
    ('64-cells (2h)',      '64-cells (2h)'),
    ('128-cells (2.25h)',  '128-cells (2.25h)'),
    ('256-cells (2.5h)',   '256-cells (2.5h)'),
    ('512-cells (2.75h)',  '512-cells (2.75h)'),
    ('1k-cells (3h)',      '1k-cells (3.h)'),
    ('high (3.3h)',        'high (3.3h)'),
    ('oblong (3.7h)',      'oblong (3.7h)'),
    ('sphere (4h)',        'sphere (4h)'),
    ('dome (4.3h)',        'dome (4.3h)'),
    ('30%-epiboly (4.7h)', '30%-epiboly (4.7h)'),
    ('50%-epiboly (5.3h)', '50%-epiboly (5.3h)'),
    ('germ ring (5.7h)',   'germ ring (5.7h)'),
    ('shield (6h)',        'shield (6h)'),
    ('75%-epiboly (8h)',   '75%-epiboly (8h)'),
    ('90%-epiboly (9h)',   '90%-epiboly (9h)'),
    ('bud (10h)',          'bud (10h)'),
    ('3-somites (11h)',    '3-somites (11h)'),
    ('6-somites (12h)',    '6-somites (12h)'),
    ('10-somites (14h)',   '10-somites (14h)'),
    ('14-somites (16h)',   '14-somites (16h)'),
    ('16-somites (18h)',   '16-somites (18h)'),
    ('21-somites (19.5h)', '21-somites (19.5h)'),
    ('26-somites (22h)',   '26-somites (22h)'),
    ('prim-6 (25h)',       'prim-6 (25h)'),
    ('prim-16 (31h)',      'prim-16 (31h)'),
    ('prim-22 (35h)',      'prim-22 (35h)'),
    ('high pec (42h)',     'high pec (42h)'),
    ('long pec (48h)',     'long pec (48h)'),

    )


# Create your models here.

#___________________________________________________________________________________________
class Parent(models.Model):
    number_of_male     = models.CharField(max_length=5, default='', help_text="Number of male")
    number_of_female   = models.CharField(max_length=5, default='', help_text="Number of female")
    number_of_unknown  = models.CharField(max_length=5, default='', help_text="Number of unknown")
    strain_name        = models.CharField(max_length=100, default='', help_text='Parent strain')
    date_of_birth      = models.DateField(null=True, help_text="Parents date of birth")
    age_at_crossing    = models.CharField(max_length=5, default='', help_text="Age at crossing in days")
    pyrat_crossing_id  = models.CharField(max_length=10, default='', help_text='Pyrat crossing id')
    mutation_grade     = models.CharField(blank=True, max_length=100, default='', help_text='Parents mutation(s)')

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}, crossID: {1}, Age at crossing: {2} days'.format(self.id, self.pyrat_crossing_id, self.age_at_crossing)

    class Meta:
        ordering = ['-id']

#___________________________________________________________________________________________
class MutationName(models.Model):
    name = models.CharField(max_length=200, default='', help_text="Name of the mutation.")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}'.format(self.name)

#___________________________________________________________________________________________
class MutationGrade(models.Model):
    grade = models.CharField(max_length=200, default='', help_text="Grade of the mutation.")
    
    class Meta:
        ordering = ('grade',)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '{0}'.format(self.grade)

#___________________________________________________________________________________________
class Mutation(models.Model):
    name  = models.ForeignKey(MutationName, on_delete=models.CASCADE, default='', help_text="Name of the mutation.")
    grade = models.ForeignKey(MutationGrade, on_delete=models.CASCADE, default='', help_text="Grade of the mutation.")

    class Meta:
        ordering = (Lower('name'),'grade',)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return '({0}, {1}, {2})'.format(self.id, self.name, self.grade)
    
#___________________________________________________________________________________________
class Treatment(models.Model):
    TREAT_TYPE = (
        ('Chemical','Chemical'),
        ('HeatShock','HeatShock'),
        ('Mechanical','Mechanical'),
        ('Light','Light'),

    )
    """Model representing a treatment"""
    name                = models.CharField(default='', max_length=200, help_text="Treatment name")
    type                = models.CharField(default='',max_length=200, help_text="Treatment type", choices=TREAT_TYPE)
    developmental_stage = models.CharField(blank=True, max_length=100, choices=DEV_STAGE, default='', help_text='Developmental stage')
    temperature         = models.CharField(blank=True, max_length=20,  default='', help_text='Treatment temperature')
    duration            = models.CharField(blank=True, max_length=20,  default='', help_text='Treatment duration')
    concentration       = models.CharField(blank=True, max_length=20,  default='', help_text='Treatment concentration')
    solvent             = models.CharField(blank=True, max_length=100,  default='', help_text='Treatment solvent')
    description         = models.TextField(blank=True, max_length=2000, help_text="Enter a description of the treatment")

    #ADD concentration

    def get_absolute_url(self):
        """Returns the url to access a particular treatment instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return "{0}, {1}, {2}, {3}".format(self.id, self.name, self.type, self.developmental_stage)

    class Meta:
        ordering = ["-id"]

#___________________________________________________________________________________________
class Injection(models.Model):
    INJC_TYPE = (
        ('Mo','Mo'),
        ('mRNA','mRNA'),
        ('CRISPR','CRISPR'),
        ('Gel','Gel'),
        ('Others','Others'),

    )
    """Model representing a treatment"""
    name                = models.CharField(default='', max_length=200, help_text="Injection name")
    type                = models.CharField(default='',max_length=200, help_text="Treatment type", choices=INJC_TYPE)
    developmental_stage = models.CharField(max_length=100, choices=DEV_STAGE, default='', help_text='Developmental stage')
    concentration       = models.CharField(blank=True, max_length=20,  default='', help_text='Injection concentration')
    slim_id             = models.CharField(blank=True, max_length=10, help_text="SLIMs ID")
    description         = models.TextField(blank=True, max_length=2000, help_text="Enter a brief description of the injection")

    def get_absolute_url(self):
        """Returns the url to access a particular injection instance."""
        return reverse('treatment-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return "{0}, {1}, {2}, {3}".format(self.id, self.name, self.type, self.developmental_stage)

    class Meta:
        ordering = ["-id"]

#___________________________________________________________________________________________
class Sample(models.Model):
    """Model representing an experiment."""  
    SPECIE_TYPE = (
        ('zebrafish',    'Zebra fish'),
    )

    specie              = models.CharField(max_length=100, choices=SPECIE_TYPE, default='zebrafish', help_text='Type of animal(s) used for this experimental dataset.')
    developmental_stage = models.CharField(max_length=100, choices=DEV_STAGE, default='', help_text='Developmental stage')
   # somite_stage        = models.CharField(max_length=100, blank=True, default='', help_text='Developmental stage')
    #ADD temperature  as a treatment type
    pyrat_crossing_id   = models.CharField(max_length=10, default='', help_text='"Pyrat crossing ID')
    mutation            = models.ManyToManyField(Mutation,  default='', help_text='mutation(s)', related_name='sample_mutation')
    parent              = models.ManyToManyField(Parent, blank=True,  default='', help_text='Parents information (automatically filled from pyrat crossing ID)')
    date_of_crossing    = models.DateField(blank=True, null=True, help_text="Date of cross (automatically filled from pyrat crossing ID)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        #parent_lines = "("+", ".join(str(par) for par in self.parent_line.all())+")"
        mutations =  ", ".join("("+str(par)+")" for par in self.mutation.all())
        return '{0}, {1}, {2}, {3}, {4}'.format(self.id, self.specie, self.developmental_stage, self.pyrat_crossing_id, mutations)

    class Meta:
        ordering = ["-id"] #("specie", "developmental_stage")



        
#___________________________________________________________________________________________
class InstrumentalCondition(models.Model):
    """Model representing the instrumental condition of a given experimental dataset."""  

    INSTRUMENTALCOND_TYPE = (
        ('microscopy',    'microscopy'),
        ('sequencing',    'sequencing'),
    )

    INSTRUMENT_NAME = (
        ('viventis1',    'viventis1'),
        ('viventis2',    'viventis2'),
        ('nikon',    'nikon'),
        ('zeiss',    'zeiss'),
        ('MiSeq',    'MiSeq'),
        ('VAST', 'VAST'),
        ('NextSeq500',    'NextSeq500'),
        ('NovaSeq6000',    'NovaSeq6000'),
    )

    TOTAL_READ = (
        ('1',     '1'),
        ('4',     '4'),
        ('15',    '15'),
        ('25',    '25'),
        ('130',   '130'),
        ('400',   '400'),
        ('800',   '800'),
        ('1600',  '1600'),
        ('4000',  '4000'),
        ('10000', '10000'),
    )

    READ_CONFIG = (
        ('50 (SR50)', '50 (SR50)'),
        ('100 (SR100)', '100 (SR100)'),
        ('60/60 (PE60)', '60/60 (PE60)'),
        ('150 (SR150)', '150 (SR150)'),
        ('100/100 (PE100)', '100/100 (PE100)'),
        ('150/150 (PE150)', '150/150 (PE150)'),
        ('250/250 (PE250)', '250/250 (PE250)'),
        ('21/90 (BRB-Seq dual index)', '21/90 (BRB-Seq dual index)'),
        ('28/90 (10XG 3\'GE v3)', '28/90 (10XG 3\'GE v3)'),
        ('26/90 (10XG 5\'GE v2)', '26/90 (10XG 5\'GE v2)'),
        ('90/90 (10XG ATAC)', '90/90 (10XG ATAC)'),
    )


    name             = models.CharField(max_length=200, default='', help_text='Name of the instrumental condition')
    instrument_type  = models.CharField(max_length=100, choices=INSTRUMENTALCOND_TYPE, default='', help_text='Type of instrument')
    instrument_name  = models.CharField(max_length=100, choices=INSTRUMENT_NAME, default='', help_text='Name of instrument')
    laser_intensity  = models.CharField(blank=True, max_length=100, default='', help_text='Laser intensity')
    laser_wavelength = models.CharField(blank=True, max_length=100, default='', help_text='Laser wave length')
    temperature      = models.CharField(blank=True, max_length=100,  default='', help_text='Instrument temperature')

    total_read  = models.CharField(blank=True,max_length=100, choices=TOTAL_READ, default='', help_text='Total number of reads')
    read_config  = models.CharField(blank=True,max_length=100, choices=READ_CONFIG, default='', help_text='Read configuration')

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""

        toret='{0}, {1}, {2}, {3}'.format(self.id, self.name, self.instrument_type, self.instrument_name)
        if self.laser_intensity!='':
            toret+=', {0}'.format(self.laser_intensity)
        if self.laser_wavelength!='':
            toret+=', {0}'.format(self.laser_wavelength)
        if self.temperature!='':
            toret+=', {0}'.format(self.temperature)
        if self.total_read!='':
            toret+=', {0}'.format(self.total_read)
        if self.read_config!='':
            toret+=', {0}'.format(self.read_config)

        return toret

    class Meta:
        #ordering = ("instrument_type", "instrument_name")
        ordering = ["-id"]


#___________________________________________________________________________________________
class ExperimentalCondition(models.Model):
    """Model representing the experimental condition of a given experimental dataset."""  
    BOOL_STATUS = (
        ('False', 'False'),
        ('True', 'True'),
    )
    sample     = models.ManyToManyField(Sample, help_text="Biological sample being used for this experimental condition")
    instrumental_condition = models.ManyToManyField(InstrumentalCondition, help_text='Instrumental conditions.')
    treatment  = models.ManyToManyField(Treatment, blank=True, help_text="Treatment(s) for this experimental condition.")
    injection  = models.ManyToManyField(Injection, blank=True, help_text="Injection(s) for this experimental condition.")
    date       = models.DateField(blank=True, null=True, help_text="Date of the experiment")
    filled     = models.CharField(max_length=10, choices=BOOL_STATUS, default='False', help_text='Set to True when all experimental conditions are properly filled')


    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        try:
            return '{0}, {1}'.format(self.experimentaldataset.raw_dataset.data_type, self.experimentaldataset.raw_dataset.data_name)
        except ObjectDoesNotExist:
            return 'none'
        
    class Meta:
        ordering = ("experimentaldataset__raw_dataset__data_type","experimentaldataset__raw_dataset__data_name")
