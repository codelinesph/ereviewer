# Generated by Django 2.1.7 on 2019-07-24 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0022_auto_20190605_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='in_public',
            field=models.BooleanField(default=True),
        ),
    ]
