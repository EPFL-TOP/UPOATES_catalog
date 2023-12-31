# Generated by Django 3.2.5 on 2023-09-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('experiment_catalog', '0001_initial'),
        ('contribution_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for the project tag', max_length=200)),
                ('name_long', models.CharField(blank=True, help_text='Long name the project tag', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the project tag', max_length=2000)),
            ],
            options={
                'verbose_name': 'Project tag',
                'verbose_name_plural': 'Project tags',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for the publication', max_length=200)),
                ('bioarxiv_id', models.CharField(help_text='Bioarxiv id for the publication using a specific experiment in the form e.g.: 2023.08.02.551629v2', max_length=200)),
                ('bioarxiv_title', models.CharField(help_text='Bioarxiv title for the publication using a specific experiment', max_length=200)),
                ('journal_id', models.CharField(blank=True, help_text='Journal id for the publication using a specific experiment', max_length=200)),
                ('journal_title', models.CharField(blank=True, help_text='Journal title for the publication using a specific experiment', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Zenodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title for the zenodo entry', max_length=200)),
                ('doi', models.CharField(help_text='Provide the zenodo DOI in the form: 10.5281/zenodo.8211680', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='Name of the project', max_length=200)),
                ('date', models.DateField(help_text='Date field in format: MM/DD/YYYY', null=True)),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('published', 'Published'), ('paused', 'Paused'), ('finished', 'Finished'), ('terminated', 'Terminated')], default='Ongoing', help_text='Status of the project', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the project', max_length=2000)),
                ('contribution', models.ManyToManyField(blank=True, help_text='Contribution(s) for this project', to='contribution_catalog.Contribution')),
                ('experimental_dataset', models.ManyToManyField(blank=True, help_text='Choose one or several experiment(s) for this project', to='experiment_catalog.ExperimentalDataset')),
                ('project_tag', models.ManyToManyField(help_text='Select project tag(s) for this experiment', to='project_catalog.ProjectTag')),
                ('publication', models.ManyToManyField(blank=True, help_text='Select publication(s) for this project', to='project_catalog.Publication')),
                ('zenodo', models.ManyToManyField(blank=True, help_text='Select zenodo(s) for this project', to='project_catalog.Zenodo')),
            ],
        ),
    ]
