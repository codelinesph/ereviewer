# Generated by Django 2.1.7 on 2019-03-01 00:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taken', '0003_auto_20190301_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attemptexam',
            name='attempted_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]