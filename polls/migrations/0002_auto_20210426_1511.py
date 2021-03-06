# Generated by Django 3.2 on 2021-04-26 08:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='percent_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'])]),
        ),
    ]
