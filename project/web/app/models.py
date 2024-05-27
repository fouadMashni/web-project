from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta

class Instructor(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='Unknown')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, default='Unknown')
    description = models.TextField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='required_for')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

    def registered_students_count(self):
        return StudentsReg.objects.filter(course=self).count()

    def available_seats(self):
        return self.capacity - self.registered_students_count()

class CourseSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    days = models.CharField(max_length=50)  
    startTime = models.TimeField()
    endTime = models.TimeField()
    roomNo = models.CharField(max_length=10)

    def get_days_list(self):
        days_mapping = {
            'Sun': 'Sunday',
            'Mon': 'Monday',
            'Tue': 'Tuesday',
            'Wed': 'Wednesday',
            'Thu': 'Thursday',
            'Fri': 'Friday',
            'Sat': 'Saturday',
            'Su': 'Sunday',
            'M': 'Monday',
            'Tu': 'Tuesday',
            'W': 'Wednesday',
            'Th': 'Thursday',
            'F': 'Friday',
            'Sa': 'Saturday'
        }
        return [days_mapping[day.strip()] for day in self.days.split(',')]

class StudentsReg(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)




class Tag(models.Model):
    name= models.CharField(max_length=90 , null= True) 
    def __str__(self):
        return self.name      


class Deadline(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

