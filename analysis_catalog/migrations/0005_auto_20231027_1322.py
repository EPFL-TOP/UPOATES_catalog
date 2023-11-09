# Generated by Django 3.2.5 on 2023-10-27 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_catalog', '0004_auto_20231027_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='Analysis tag name', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Analysis tag description', max_length=2000)),
            ],
            options={
                'verbose_name': 'Analysis tag',
                'verbose_name_plural': 'Analysis tags',
            },
        ),
        migrations.AddField(
            model_name='analysis',
            name='analysis_tag',
            field=models.ManyToManyField(help_text='Analysis tag(s) for this analysis', to='analysis_catalog.AnalysisTag'),
        ),
    ]
