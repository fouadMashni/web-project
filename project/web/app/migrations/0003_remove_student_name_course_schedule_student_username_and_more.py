# Generated by Django 5.0.4 on 2024-05-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_course_instructor_courseschedule_course_instructor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.AddField(
            model_name='course',
            name='schedule',
            field=models.CharField(default='Not scheduled', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(default='username', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.IntegerField(max_length=100, unique=True),
        ),
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, to='app.course'),
        ),
    ]
