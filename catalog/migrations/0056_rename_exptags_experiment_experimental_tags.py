# Generated by Django 3.2.5 on 2023-08-04 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0055_auto_20230804_1041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='exptags',
            new_name='experimental_tags',
        ),
    ]
