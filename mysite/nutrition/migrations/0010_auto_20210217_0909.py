# Generated by Django 3.1.3 on 2021-02-17 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0009_auto_20210217_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
