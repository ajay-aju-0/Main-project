# Generated by Django 3.2.4 on 2023-04-19 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_sickness_details_consumption'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferdetails',
            name='order',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='pdate',
            field=models.DateField(verbose_name='Purchase Date'),
        ),
    ]
