# Generated by Django 3.2.5 on 2023-08-03 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawdata_catalog', '0045_contribution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='orcid_id',
            new_name='orcid',
        ),
    ]
