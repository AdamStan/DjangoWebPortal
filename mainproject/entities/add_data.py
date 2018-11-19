from .models import *
from accounts.models import User

def add_data():
    faculty1 = Faculty(name="EEIA")
    faculty1.save()
    teachers = User.objects.get(teacher=True)
    teachers_list = []
    for t in teachers:
        teachers_list.append(Teacher(user=t, faculty=faculty1))
        teachers_list[-1].save()
    field_of_study1 = FieldOfStudy(name="Computer Science", degree = FieldOfStudy.BACHELOR, faculty=faculty1)
    field_of_study2 = FieldOfStudy(name="Computer Science", degree = FieldOfStudy.MASTER, faculty=faculty1)
    field_of_study1.save()
    field_of_study2.save()

    subject_list = []
    subject_list.append(Subject(name="Mathematics 1", semester=1, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Safety at Work and Ergonomics", semester=1, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Physics", semester=1, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Introduction to Computer Science", semester=1, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Scripting Languages", semester=1, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Algorithms and Data Structures", semester=1, fieldOfStudy=field_of_study1))

    subject_list.append(Subject(name="Mathematics 2", semester=2, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Safety at Work and Ergonomics", semester=2, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Physics", semester=2,fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Introduction to Computer Science", semester=2,fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Scripting Languages", semester=2,fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Algorithms and Data Structures", semester=2,fieldOfStudy=field_of_study1))