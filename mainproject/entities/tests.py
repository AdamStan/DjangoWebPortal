from django.test import TestCase
from .models import *
from accounts.models import User

# Create your tests here.
class TestEntities(TestCase):
    def setUp(self):
        faculty1 = Faculty(name="EEIA")
        faculty1.save()
        teacher = User.objects.create_teacher(
            username="teacher_x",
            password="teacher_user",
            name="Jan",
            surname="Kowalski"
        )
        teacher.save()

        field_of_study = FieldOfStudy(name="Computer Science", degree = FieldOfStudy.BACHELOR, faculty=faculty1)
        field_of_study.save()

        subject_list = []
        # 1st semester - field_of_study1
        subject_list.append(
            Subject(name="Mathematics 1", semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name="Safety at Work and Ergonomics", semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name="Physics", semester=1, fieldOfStudy=field_of_study, lecture_hours=30, laboratory_hours=30)
        )
        subject_list.append(
            Subject(name="Introduction to Computer Science", semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name="Scripting Languages", semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name="Algorithms and Data Structures", semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=3)
        )

        for sub in subject_list:
            sub.save()

        plan_list = []
        plan_list.append(Plan(title="CS1_01", fieldOfStudy=field_of_study, semester=1))
        plan_list.append(Plan(title="CS1_02", fieldOfStudy=field_of_study, semester=1))
        plan_list.append(Plan(title="CS1_03", fieldOfStudy=field_of_study, semester=1))

        for p in plan_list:
            p.save()

        subjects = Subject.objects.filter(fieldOfStudy=field_of_study)

        scheduled_subject_list = []
        for p in plan_list:
            for s in subjects:
                scheduled_subject_list.append(
                    ScheduledSubject(subject=s, plan=p)
                )

        for ss in scheduled_subject_list:
            ss.save()


    def test_faculty(self):
        faculty = Faculty.objects.get(name="EEIA")
        self.assertIsNotNone(faculty)
        try:
            faculty = Faculty.objects.get(name="Does not exist")
        except Exception:
            self.assertEquals(True, True)




