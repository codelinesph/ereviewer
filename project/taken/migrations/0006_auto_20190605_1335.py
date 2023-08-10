# Generated by Django 2.1.7 on 2019-06-05 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_auto_20190605_1335'),
        ('taken', '0005_auto_20190415_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptexam',
            name='course_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Course'),
        ),
        migrations.AddField(
            model_name='attemptexam',
            name='subject_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Subject'),
        ),
        migrations.AddField(
            model_name='attemptexam',
            name='topic_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Topics'),
        ),
    ]
