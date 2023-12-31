# Generated by Django 3.2.5 on 2023-09-21 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentalcondition_catalog', '0002_parent_number_of_male'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumentalcondition',
            name='instrument_name',
            field=models.CharField(choices=[('viventis1', 'viventis1'), ('viventis2', 'viventis2'), ('nikon', 'nikon'), ('zeiss', 'zeiss'), ('MiSeq', 'MiSeq'), ('VAST', 'VAST'), ('NextSeq500', 'NextSeq500'), ('NovaSeq6000', 'NovaSeq6000')], default='', help_text='Name of instrument', max_length=100),
        ),
    ]
