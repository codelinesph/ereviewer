# Generated by Django 2.1.7 on 2019-04-15 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_course_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='content',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]