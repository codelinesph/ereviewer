# Generated by Django 2.1.7 on 2019-05-03 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_auto_20190503_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['arrangement']},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['arrangement'], 'verbose_name': 'Lesson', 'verbose_name_plural': 'Topic Lessons'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['arrangement']},
        ),
        migrations.AlterModelOptions(
            name='topics',
            options={'ordering': ['arrangement'], 'verbose_name': 'Topic', 'verbose_name_plural': 'Subject Topics'},
        ),
    ]
