# Generated by Django 3.2.4 on 2023-04-11 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20230411_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='zootimings',
            name='holiday',
            field=models.BooleanField(default=False),
        ),
    ]