# Generated by Django 2.1.7 on 2019-04-05 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='banner',
            field=models.ImageField(null=True, upload_to='www/img-cdn/subjects/banners//%Y/%m/%d'),
        ),
    ]
