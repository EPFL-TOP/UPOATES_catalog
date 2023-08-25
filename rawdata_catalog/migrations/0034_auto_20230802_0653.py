# Generated by Django 3.2.5 on 2023-08-02 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rawdata_catalog', '0033_auto_20230731_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='type',
        ),
        migrations.AlterField(
            model_name='contributor',
            name='orcid_id',
            field=models.CharField(blank=True, default='', help_text='Provide 16 digits orcid in the form: 0000-0000-0000-0000', max_length=100),
        ),
    ]
