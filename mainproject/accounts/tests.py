from django.test import TestCase
from .models import User
# Create your tests here.
# there will be creating users
class UserTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            username="admin123",
            password="haslo123",
            name="admin_name",
            surname="admin_surname"
        )
        User.objects.create_teacher(
        )
        User.objects.create_teacher()
        User.objects.create_teacher()
        User.objects.create_teacher()
        User.objects.create_teacher()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()
        User.objects.create_student()

    def test_admins(self):
        pass

    def test_teachers(self):
        pass

    def test_students(self):
        pass
