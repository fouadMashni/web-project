# Generated by Django 5.0.4 on 2024-05-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_student_name_course_schedule_student_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='student',
            name='username',
        ),
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
