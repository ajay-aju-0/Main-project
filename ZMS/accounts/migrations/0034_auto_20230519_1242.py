# Generated by Django 3.2.4 on 2023-05-19 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_alter_dismantledenclosures_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dismantledenclosures',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='dismantledenclosures',
            name='reason',
            field=models.CharField(max_length=200, verbose_name='Dismantle reason'),
        ),
    ]