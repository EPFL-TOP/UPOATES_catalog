# Generated by Django 3.2.5 on 2023-09-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentalcondition_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='number_of_male',
            field=models.CharField(default='', help_text='Number of male', max_length=5),
        ),
    ]