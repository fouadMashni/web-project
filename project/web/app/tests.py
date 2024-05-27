# app/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from app.models import Student, Course, Instructor, StudentsReg

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='student')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Student.objects.filter(email='testuser@example.com').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Testpassword123')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

class CourseSearchTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(name='John Doe')
        self.course = Course.objects.create(code='CS101', name='Intro to Computer Science', description='Intro course', instructor=self.instructor, capacity=30)

    def test_search_by_course_code(self):
        response = self.client.get(reverse('search'), {'query': 'CS101'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Intro to Computer Science')

    def test_search_by_course_name(self):
        response = self.client.get(reverse('search'), {'query': 'Intro to Computer Science'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Intro to Computer Science')

class CourseRegistrationTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='student')
        self.user = User.objects.create_user(username='testuser', password='Testpassword123')
        self.student = Student.objects.create(user=self.user, name='Test Student', email='teststudent@example.com')
        self.instructor = Instructor.objects.create(name='John Doe')
        self.course = Course.objects.create(code='CS101', name='Intro to Computer Science', description='Intro course', instructor=self.instructor, capacity=30)
        self.client.login(username='testuser', password='Testpassword123')

    def test_register_to_course(self):
        response = self.client.post(reverse('register_to_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StudentsReg.objects.filter(student=self.student, course=self.course).exists())
    