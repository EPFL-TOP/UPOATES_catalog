# Generated by Django 3.2.5 on 2023-08-04 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawdata_catalog', '0056_rename_exptags_experiment_experimental_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='data type',
            new_name='data_type',
        ),
    ]
