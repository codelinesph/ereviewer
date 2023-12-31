# Generated by Django 2.1.7 on 2019-03-01 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taken', '0002_auto_20190227_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptexam',
            name='attempted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='attemptquestion',
            name='points',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
