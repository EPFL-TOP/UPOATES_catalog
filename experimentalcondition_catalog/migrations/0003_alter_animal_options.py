# Generated by Django 3.2.5 on 2023-09-11 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experimentalcondition_catalog', '0002_auto_20230911_1400'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'ordering': ['specie', 'developmental_stage']},
        ),
    ]
