# Generated by Django 3.0.3 on 2020-03-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('larps', '0011_auto_20200327_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uniform',
            name='gender',
        ),
        migrations.AddField(
            model_name='uniformsize',
            name='gender',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]