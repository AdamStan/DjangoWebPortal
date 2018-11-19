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
        admin = User.objects.get(admin=True)
        self.assertEqual(admin.username, 'admin_x')
        self.assertEqual(admin.admin, True)
        self.assertEqual(admin.staff, True)

    def test_teachers(self):
        teacher = User.objects.get(teacher=True)
        self.assertEqual(teacher.teacher, True)
        self.assertEqual(teacher.staff, False)

    def test_students(self):
        student = User.objects.get(student=True)
        self.assertEqual(student.student, True)
        self.assertEqual(student.staff, False)
