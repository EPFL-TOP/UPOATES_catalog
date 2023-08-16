# Generated by Django 3.2.5 on 2023-08-05 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0061_auto_20230805_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='status',
            new_name='experiment_status',
        ),
        migrations.AddField(
            model_name='experiment',
            name='data_status',
            field=models.CharField(choices=[('available', 'Available'), ('notavailable', 'Not available'), ('deleted', 'Deleted')], default='', help_text='Status of the data on the RCP storage', max_length=100),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a brief description of the contribution for this contributor', max_length=2000),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a brief description of the experiment', max_length=2000),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a brief description of the treatment', max_length=2000),
        ),
    ]
