# Generated by Django 3.2.5 on 2023-09-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specie', models.CharField(choices=[('zebrafish', 'Zebra fish')], default='zebrafish', help_text='Type of animal(s) used for this experimental dataset.', max_length=100)),
                ('developmental_stage', models.CharField(choices=[('2cells', '2 Cells'), ('4cells', '4 Cells'), ('8cells', '8 Cells'), ('12somites', '12 Somites')], default='', help_text='Developmental stage', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Injection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for injection', max_length=200)),
                ('developmental_stage', models.CharField(choices=[('2cells', '2 Cells'), ('4cells', '4 Cells'), ('8cells', '8 Cells'), ('12somites', '12 Somites')], default='', help_text='Developmental stage', max_length=100)),
                ('name_long', models.CharField(blank=True, help_text='Long name for injection', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the injection', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Mutation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for the fish line', max_length=200)),
                ('name_long', models.CharField(blank=True, help_text='Long name for fish line', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the fish line', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='MutationGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for the fish line', max_length=200)),
                ('name_long', models.CharField(blank=True, help_text='Long name for fish line', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the fish line', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='ParentLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for the fish line', max_length=200)),
                ('name_long', models.CharField(blank=True, help_text='Long name for fish line', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the fish line', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_short', models.CharField(help_text='Short name for treatment', max_length=200)),
                ('developmental_stage', models.CharField(choices=[('2cells', '2 Cells'), ('4cells', '4 Cells'), ('8cells', '8 Cells'), ('12somites', '12 Somites')], default='', help_text='Developmental stage', max_length=100)),
                ('name_long', models.CharField(blank=True, help_text='Long name for treatment', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the treatment', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Experimentalcondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal', models.ManyToManyField(help_text='Species used', to='experimentalcondition_catalog.Animal')),
                ('injection', models.ManyToManyField(blank=True, help_text='Injection(s) for this experimental dataset.', to='experimentalcondition_catalog.Injection')),
                ('treatment', models.ManyToManyField(blank=True, help_text='Treatment(s) for this experimental dataset.', to='experimentalcondition_catalog.Treatment')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='mutation',
            field=models.ManyToManyField(help_text='mutation', to='experimentalcondition_catalog.Mutation'),
        ),
        migrations.AddField(
            model_name='animal',
            name='mutation_grade',
            field=models.ManyToManyField(help_text='mutation grade', to='experimentalcondition_catalog.MutationGrade'),
        ),
        migrations.AddField(
            model_name='animal',
            name='parent_line',
            field=models.ManyToManyField(help_text='Parents fish lines', to='experimentalcondition_catalog.ParentLine'),
        ),
    ]
