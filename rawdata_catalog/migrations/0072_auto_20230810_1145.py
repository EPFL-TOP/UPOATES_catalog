# Generated by Django 3.2.5 on 2023-08-10 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawdata_catalog', '0071_auto_20230810_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='book',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
