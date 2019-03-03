from django.test import TestCase
from ..models import *
from accounts.models import User


# Create your tests here.
class TestEntities(TestCase):
    subjects_names = [
        "Mathematics 1",
        "Safety at Work and Ergonomics",
        "Physics",
        "Introduction to Computer Science",
        "Scripting Languages",
        "Algorithms and Data Structures"
    ]

    def setUp(self):
        faculty1 = Faculty(name="EEIA")
        faculty1.save()
        user_teacher = User.objects.create_teacher(
            username="teacher_x",
            password="teacher_user",
            name="Jan",
            surname="Kowalski"
        )
        user_teacher.save()
        teacher = Teacher(user=user_teacher, faculty=faculty1)
        teacher.save()

        field_of_study = FieldOfStudy(name="Computer Science", degree = FieldOfStudy.BACHELOR, faculty=faculty1)
        field_of_study.save()

        subject_list = []
        # 1st semester - field_of_study1
        subject_list.append(
            Subject(name=TestEntities.subjects_names[0], semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name=TestEntities.subjects_names[1], semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name=TestEntities.subjects_names[2], semester=1, fieldOfStudy=field_of_study, lecture_hours=30, laboratory_hours=30)
        )
        subject_list.append(
            Subject(name=TestEntities.subjects_names[3], semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name=TestEntities.subjects_names[4], semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=30)
        )
        subject_list.append(
            Subject(name=TestEntities.subjects_names[5], semester=1, fieldOfStudy=field_of_study, lecture_hours=30,laboratory_hours=3)
        )

        for sub in subject_list:
            sub.save()
            sub.teachers.add(teacher)

        plan_list = []
        plan_list.append(Plan(title="CS1_01", fieldOfStudy=field_of_study, semester=1))
        plan_list.append(Plan(title="CS1_02", fieldOfStudy=field_of_study, semester=1))
        plan_list.append(Plan(title="CS1_03", fieldOfStudy=field_of_study, semester=1))

        for p in plan_list:
            p.save()

        subjects = Subject.objects.filter(fieldOfStudy=field_of_study, semester=1)

        scheduled_subject_list = []
        for p in plan_list:
            for s in subjects:
                if s.lecture_hours > 0:
                    scheduled_subject_list.append(
                        ScheduledSubject(subject=s, plan=p, type=ScheduledSubject.LECTURE)
                    )
                if s.laboratory_hours > 0:
                    scheduled_subject_list.append(
                        ScheduledSubject(subject=s, plan=p, type=ScheduledSubject.LABORATORY)
                    )

        for ss in scheduled_subject_list:
            ss.save()

        building = Building(
            name="MainBuilding",
            city="Łódź",
            street="ul. Napoleaona",
            numberOfBuilding='12a',
            postalCode='90-023',
        )
        building.save()

        room1 = Room(id='r001', building=building, room_type=Room.LABORATORY)
        room2 = Room(id='r002', building=building, room_type=Room.LECTURE)
        room1.save()
        room2.save()

    def test_faculty(self):
        faculty = Faculty.objects.get(name="EEIA")
        self.assertIsNotNone(faculty)
        try:
            faculty = Faculty.objects.get(name="Does not exist")
        except Exception:
            self.assertEquals(True, True)

    def test_teacher(self):
        teacher = Teacher.objects.get(user__username="teacher_x")
        self.assertIsNotNone(teacher)

    def test_subjects(self):
        for name in TestEntities.subjects_names:
            subject = Subject.objects.get(name=name)
            self.assertIsNotNone(subject)

