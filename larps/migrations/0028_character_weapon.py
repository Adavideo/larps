# Generated by Django 3.1.3 on 2021-01-03 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('larps', '0027_remove_character_weapon'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='weapon',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
