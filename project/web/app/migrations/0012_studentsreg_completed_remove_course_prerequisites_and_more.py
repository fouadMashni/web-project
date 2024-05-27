# Generated by Django 5.0.4 on 2024-05-23 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsreg',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.AlterUniqueTogether(
            name='studentsreg',
            unique_together={('student', 'course')},
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, to='app.course'),
        ),
    ]
