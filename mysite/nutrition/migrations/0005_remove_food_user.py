# Generated by Django 3.1.3 on 2021-02-09 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0004_auto_20210208_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='user',
        ),
    ]
