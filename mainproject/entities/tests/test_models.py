from django.test import TestCase
from datetime import time
from ..models import Faculty, FieldOfStudy, Subject, Building, Room, Plan, ScheduledSubject


class CheckModelsEquals(TestCase):

    def setUp(self):
        self.faculty = Faculty(name="WEEIA")
        self.field_of_study = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                           degree=FieldOfStudy.BACHELOR, howManySemesters=2,
                                           whenDoesItStarts=FieldOfStudy.WINTER)

    def test_check_faculty_are_not_equal(self):
        faculty1 = Faculty(name="WEEIA", description="Wydzial elektroniki, elektrotechniki, informaytki itd")
        faculty2 = Faculty(name="WM", description="Wydzial mechaniczny")
        self.assertNotEqual(faculty1, faculty2, "Faculties should not be equal")

    def test_check_faculty_are_equal(self):
        faculty1 = Faculty(name="WEEIA")
        faculty2 = Faculty(name="WEEIA")
        self.assertEqual(faculty1, faculty2, "There are the same faculties")

    def test_check_fieldsOfStudy_are_equal(self):
        field_of_study1 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=7,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        field_of_study2 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=7,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        self.assertEqual(field_of_study1, field_of_study2, "Fields are not the same")

    def test_check_fieldsOfStudy_are_not_equal(self):
        field_of_study1 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=2,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        field_of_study2 = FieldOfStudy(name="Computer Science", faculty=self.faculty,
                                       degree=FieldOfStudy.BACHELOR, howManySemesters=7,
                                       whenDoesItStarts=FieldOfStudy.WINTER)
        self.assertNotEqual(field_of_study1, field_of_study2, "Fields are equal")

    def test_check_subjects_are_equal(self):
        subject1 = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        subject2 = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        self.assertEqual(subject1, subject2, "Subjects are not equal!")

    def test_check_subjects_are_not_equal(self):
        subject1 = Subject(name="SubjectName123", fieldOfStudy=self.field_of_study, semester=6)
        subject2 = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        self.assertNotEqual(subject1, subject2, "Subjects are equal!")

    def test_check_buildings_are_equal(self):
        building1 = Building(name="name",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        building2 = Building(name="name",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        self.assertEqual(building1, building2, "Buildings are not equal!")

    def test_check_building_are_not_equal(self):
        building1 = Building(name="name1",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        building2 = Building(name="name2",city="city",street="street",numberOfBuilding="12a",postalCode="27-340")
        self.assertNotEqual(building1, building2, "Buildings are equal!")

    def test_check_rooms_are_equal(self):
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room1 = Room(id="b10_12",building=building,room_type=Room.LECTURE)
        room2 = Room(id="b10_12",building=building,room_type=Room.LECTURE)
        self.assertEqual(room1, room2, "Rooms are not equal!")

    def test_rooms_are_not_equal(self):
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room1 = Room(id="b10_12", building=building, room_type=Room.LECTURE)
        room2 = Room(id="b10_13", building=building, room_type=Room.LECTURE)
        self.assertNotEqual(room1, room2, "Rooms are equal!")

    def test_plans_are_equal(self):
        plan1 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        plan2 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        self.assertEqual(plan1, plan2, "Plans are not equal!")

    def test_plans_are_not_equal(self):
        plan1 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        plan2 = Plan(title="CS2_02", fieldOfStudy=self.field_of_study, semester=2)
        self.assertNotEqual(plan1, plan2, "Plans are equal!")

    def test_scheduled_subject_are_equal(self):
        subject = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        plan = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room = Room(id="b10_12", building=building, room_type=Room.LECTURE)
        event1 = ScheduledSubject(subject=subject, plan=plan, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        event2 = ScheduledSubject(subject=subject, plan=plan, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        self.assertEqual(event1, event2, "Scheduled Subjects are not equal!")

    def test_scheduled_subject_are_not_equal(self):
        subject = Subject(name="SubjectName", fieldOfStudy=self.field_of_study, semester=6)
        plan1 = Plan(title="CS2_01", fieldOfStudy=self.field_of_study, semester=2)
        plan2 = Plan(title="CS2_02", fieldOfStudy=self.field_of_study, semester=2)
        building = Building(name="name", city="city", street="street", numberOfBuilding="12a", postalCode="27-340")
        room = Room(id="b10_12", building=building, room_type=Room.LECTURE)
        event1 = ScheduledSubject(subject=subject, plan=plan1, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        event2 = ScheduledSubject(subject=subject, plan=plan2, room=room,
                                  whenStart=time(12,0,0), whenFinnish=time(14,0,0), dayOfWeek=2)
        self.assertNotEqual(event1, event2, "Scheduled Subjects are equal!")

