from django.contrib import admin
from .models import  Course, CourseSchedule, Instructor, Student, StudentsReg, Notification, Deadline


admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(StudentsReg)
admin.site.register(Student)
admin.site.register(Notification)
admin.site.register(Deadline)
