from django.test import TestCase
from .models import User
# Create your tests here.
# there will be creating users
class UserTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            username="admin_x",
            password="haslo123",
            name="admin_name",
            surname="admin_surname"
        )
        User.objects.create_teacher(
            username="teacher_x",
            password="teacher_user",
            name="Jan",
            surname="Kowalski"
        )
        User.objects.create_student(
            username="student_x",
            password="student_user",
            name="Katarzyna",
            surname="Popowska"
        )

    def test_admins(self):
        pass

    def is_admin_a_staff(self):
        pass

    def test_teachers(self):
        pass

    def is_teacher_a_staff(self):
        pass

    def test_students(self):
        pass

    def is_student_a_staff(self):
        pass
