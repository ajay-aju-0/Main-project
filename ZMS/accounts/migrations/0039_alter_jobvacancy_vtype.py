# Generated by Django 3.2.4 on 2023-05-26 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_alter_jobvacancy_qualification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobvacancy',
            name='vtype',
            field=models.CharField(choices=[('temporary', 'temporary'), ('permanent', 'permanent')], max_length=10, verbose_name='Vacancy Type'),
        ),
    ]
