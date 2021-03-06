# Generated by Django 3.1.3 on 2020-11-10 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('larps', '0013_player_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='allergies',
        ),
        migrations.RemoveField(
            model_name='player',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='player',
            name='dietary_restrictions',
        ),
        migrations.RemoveField(
            model_name='player',
            name='emergency_contact',
        ),
        migrations.RemoveField(
            model_name='player',
            name='food_allergies',
        ),
        migrations.RemoveField(
            model_name='player',
            name='food_intolerances',
        ),
        migrations.RemoveField(
            model_name='player',
            name='medical_conditions',
        ),
        migrations.DeleteModel(
            name='DietaryRestriction',
        ),
    ]
