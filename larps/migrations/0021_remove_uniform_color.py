# Generated by Django 3.1.3 on 2020-11-21 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('larps', '0020_merge_20201122_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uniform',
            name='color',
        ),
    ]