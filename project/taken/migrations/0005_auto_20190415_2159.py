# Generated by Django 2.1.7 on 2019-04-15 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taken', '0004_auto_20190301_0818'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attemptexam',
            options={'ordering': ['pk']},
        ),
    ]