from django.urls import path
from . import views

urlpatterns = [ 

    path('',views.main),
    path('Register/', views.register, name='register'),
    path('LogIn/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('Course/', views.course, name='course'),
    path('Search/',views.course_search , name='search'),
    path('main/',views.main , name='main'),
    path('register/<int:course_id>/', views.register_to_course, name='register_to_course'),
    path('unregister/<int:course_id>/', views.unregister_from_course, name='unregister_from_course'),
    path('Registeredcourses/', views.view_registered_courses, name='view_registered_courses'),
    path('schedules/', views.schedules_view, name='schedules')
]


