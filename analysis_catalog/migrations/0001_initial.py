# Generated by Django 3.2.5 on 2023-10-19 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_catalog', '0004_auto_20231006_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the analysis dataset', max_length=100)),
                ('path', models.CharField(help_text='Path of the analysis dataset', max_length=200)),
                ('number_of_files', models.CharField(help_text='Path of the analysis dataset', max_length=200)),
                ('total_size', models.CharField(help_text='Path of the analysis dataset', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the analysis.', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Description of the experiment', max_length=2000)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_catalog.project')),
            ],
        ),
    ]
