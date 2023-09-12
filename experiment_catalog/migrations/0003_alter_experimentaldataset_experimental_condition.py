# Generated by Django 3.2.5 on 2023-09-08 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experimentalcondition_catalog', '0001_initial'),
        ('experiment_catalog', '0002_auto_20230908_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentaldataset',
            name='experimental_condition',
            field=models.OneToOneField(blank=True, default='', help_text='Raw dataset for this experimental dataset.', null=True, on_delete=django.db.models.deletion.CASCADE, to='experimentalcondition_catalog.experimentalcondition'),
        ),
    ]
