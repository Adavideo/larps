# Generated by Django 3.0.3 on 2020-03-25 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('larps', '0005_bookings_bus'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='sleeping_bag',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
