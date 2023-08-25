# Generated by Django 3.2.5 on 2023-08-10 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawdata_catalog', '0070_auto_20230810_1108'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
