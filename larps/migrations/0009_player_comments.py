# Generated by Django 3.0.3 on 2020-03-25 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('larps', '0008_auto_20200325_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='comments',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
