# Generated by Django 3.2.5 on 2023-09-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.CharField(help_text='Type of data for this dataset (reflecting the the RCP storage categories)', max_length=100)),
                ('data_name', models.CharField(help_text='Name of the experimental dataset folder on the RCP storage.', max_length=100)),
                ('number_of_files', models.CharField(default='', help_text='Number of files for this dataset.', max_length=10)),
                ('total_size', models.CharField(default='', help_text='Total size for this dataset (in bytes).', max_length=100)),
                ('data_status', models.CharField(choices=[('available', 'Available'), ('notavailable', 'Not available'), ('deleted', 'Deleted')], default='', help_text='Status of the data on the RCP storage.', max_length=100)),
                ('date_added', models.DateField(help_text='Date automatically registered (when pushing the refresh button)', null=True)),
                ('date_removed', models.DateField(help_text='Date when the rawdataset is removed from RCP', null=True)),
                ('files_data', models.JSONField(null=True)),
                ('compression', models.CharField(blank=True, choices=[('none', 'None'), ('jeraw', 'JetRaw'), ('zip', 'Zip'), ('tar', 'Tar')], default='', help_text='Type of compression if any', max_length=100)),
                ('file_format', models.CharField(blank=True, choices=[('none', 'None'), ('tiff', 'tiff'), ('nd2', 'nd2'), ('fastq', 'fastq')], default='', help_text='Format of the files', max_length=100)),
            ],
            options={
                'ordering': ('data_type', 'data_name'),
            },
        ),
    ]
