# Generated by Django 3.2.4 on 2023-04-22 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_consumptiondetails_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketRateHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catagory', models.CharField(max_length=20)),
                ('rate', models.IntegerField()),
                ('updated_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
