# Generated by Django 3.2.4 on 2023-04-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_users_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='country',
            field=models.CharField(max_length=32),
        ),
    ]
