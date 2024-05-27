from email.headerregistry import Group
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from .models import *  
from .forms import * 
from  django.contrib.auth.decorators import login_required 
from .decorators import * 
from django.shortcuts import redirect, get_object_or_404, render
from datetime import timedelta
from django.utils import timezone


def course_search(request):
    return render(request, 'app/Search.html', {'course': Course.objects.prefetch_related('courseschedule_set').all()})

def main(request):
   return render (request,"app/main.html")

def course(request):
    courses = Course.objects.all()  
    return render(request, 'app/Course.html', {'courses': courses})

@login_required
def register_to_course(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    prerequisites = course.prerequisites.all()
    for prereq in prerequisites:
        if not StudentsReg.objects.filter(student=student, course=prereq, completed=True).exists():
            messages.error(request, f"You cannot register for {course.name} until you have completed the prerequisite course {prereq.name}.")
            return redirect('course')  
    if not StudentsReg.objects.filter(student=student, course=course).exists():
        StudentsReg.objects.create(student=student, course=course)
        Notification.objects.create(user=request.user, message=f"You have registered for the course: {course.name}")
        messages.success(request, f"You have successfully registered for the course: {course.name}.")
    else:
        messages.info(request, f"You are already registered for the course: {course.name}.")
    return redirect('course')

@login_required
def unregister_from_course(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    registrations = StudentsReg.objects.filter(student=student, course=course)
    if registrations.exists():
        registrations.delete()
        Notification.objects.create(user=request.user, message=f"You have unregistered from the course: {course.name}")
        messages.success(request, f"You have successfully unregistered from the course: {course.name}.")
    else:
        messages.info(request, f"You are not registered for the course: {course.name}.")
    return redirect('view_registered_courses')

@login_required
def view_registered_courses(request):
    registrations = StudentsReg.objects.filter(student=request.user.student)
    return render(request, 'app/Registeredcourses.html', {'registrations': registrations})

def register(request):
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="student")
            user.groups.add(group)
            messages.success(request, f"Account created successfully for {user.username}")
            return redirect('login')
    else:
        form = CreateNewUser()
    return render(request, 'app/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'app/login.html')

def dashboard(request):
    notifications = Notification.objects.filter(user=request.user, read=False).order_by('-timestamp')
    
    now = timezone.now()
    upcoming_deadlines = Deadline.objects.filter(due_date__gte=now, due_date__lte=now + timedelta(days=7))

    context = {
        'student': request.user.student,  
        'notifications': notifications,
        'upcoming_deadlines': upcoming_deadlines,
    }
    
    return render(request, 'app/dashboard.html', context)

def schedules_view(request):
    student = request.user.student  
    registered_courses = StudentsReg.objects.filter(student=student).values_list('course', flat=True)
    schedules = CourseSchedule.objects.filter(course__in=registered_courses)
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    context = {
        'schedules': schedules,
        'days_of_week': days_of_week
    }
    return render(request, 'app/schedules.html', context)

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.info(request, "Your session has expired. Please log in again.")
    return redirect('main')