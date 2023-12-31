# Generated by Django 2.1.7 on 2019-06-05 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_auto_20190601_0815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['arrangement'], 'verbose_name': 'Lesson', 'verbose_name_plural': 'Topic Lessons'},
        ),
        migrations.AlterModelOptions(
            name='topics',
            options={'ordering': ['arrangement'], 'verbose_name': 'Topic', 'verbose_name_plural': 'Subject Topics'},
        ),
        migrations.AddField(
            model_name='course',
            name='assessment_limit',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
    ]
