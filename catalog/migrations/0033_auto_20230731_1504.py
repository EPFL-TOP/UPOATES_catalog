# Generated by Django 3.2.5 on 2023-07-31 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_auto_20230731_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(help_text='Origin of contribution', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='contributor',
            name='type',
            field=models.ManyToManyField(help_text='Select one or several type for this contributor', to='catalog.Type'),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='affiliation',
            field=models.ManyToManyField(help_text='Select one or several affiliation(s) for this contributor', to='catalog.Affiliation'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='origin',
            field=models.ManyToManyField(help_text='Select one or several origin for this contributor', to='catalog.Origin'),
        ),
    ]
