# Generated by Django 3.2.5 on 2023-09-17 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rawdata_catalog', '0003_rawdataset_date_removed'),
        ('experimentalcondition_catalog', '__first__'),
        ('contribution_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_name', models.CharField(help_text='Name of the experiment.', max_length=100)),
                ('date', models.DateField(help_text='Date of the experiment.', null=True)),
                ('description', models.TextField(blank=True, help_text='Description of the experiment', max_length=2000)),
                ('contribution', models.ManyToManyField(blank=True, help_text='Contribution(s) for this experiment', to='contribution_catalog.Contribution')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentalTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for the experimental tag', max_length=200)),
                ('name_long', models.CharField(blank=True, help_text='Long name the experimental tag', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the experimental tag', max_length=2000)),
            ],
            options={
                'verbose_name': 'Experimental tag',
                'verbose_name_plural': 'Experimental tags',
            },
        ),
        migrations.CreateModel(
            name='ExperimentalDataset',
            fields=[
                ('raw_dataset', models.OneToOneField(help_text='Raw dataset for this experimental dataset.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rawdata_catalog.rawdataset')),
                ('experiment', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='experiment_catalog.experiment')),
                ('experimental_condition', models.OneToOneField(blank=True, default='', help_text='Raw dataset for this experimental dataset.', null=True, on_delete=django.db.models.deletion.CASCADE, to='experimentalcondition_catalog.experimentalcondition')),
            ],
            options={
                'ordering': ('raw_dataset__data_type', 'raw_dataset__data_name'),
            },
        ),
        migrations.AddField(
            model_name='experiment',
            name='experimental_tag',
            field=models.ManyToManyField(help_text='Experimental tag(s) for this experiment', to='experiment_catalog.ExperimentalTag'),
        ),
    ]