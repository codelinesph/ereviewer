# Generated by Django 2.1.7 on 2019-04-09 00:45

import content.models.course
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20190405_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='banner',
            field=models.ImageField(null=True, upload_to=content.models.course.get_banner_path),
        ),
        migrations.AddField(
            model_name='course',
            name='logo',
            field=models.ImageField(null=True, upload_to=content.models.course.get_logo_path),
        ),
    ]