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
    # 1st semester - field_of_study1
    subject_list.append(Subject(name="Mathematics 1", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Safety at Work and Ergonomics", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Physics", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Introduction to Computer Science", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Scripting Languages", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Algorithms and Data Structures", semester=1, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    # 2nd semester - field_of_study1
    subject_list.append(Subject(name="Mathematics 2", semester=2, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Programming and Data Structures", semester=2, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Electrical Circuits and Measurements", semester=2,fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Modern Physics", semester=2,fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Scripting Languages 2", semester=2,fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Java Fundamentals", semester=2,fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    # 3rd semester - field_of_study1
    subject_list.append(Subject(name="Electronics Fundamentals", semester=3, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Digital Systems", semester=3, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Object Oriented Programming in C++", semester=3, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Databases", semester=3, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Mathematics 3", semester=3, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Image Processing", semester=3, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    # 4th semester - field_of_study1
    subject_list.append(Subject(name="Numerical Methods", semester=4, fieldOfStudy=field_of_study1, lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computer Architecture", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Interactive Web Applications", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Software Engineering", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Team Project", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="GUI Programming", semester=4, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    # 5th semester - field_of_study1
    subject_list.append(Subject(name="Economics", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Operating Systems", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computer Networks", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computer Aided Design", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Embedded Systems", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computer Graphics", semester=5, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    # 6th semester - field_of_study1
    subject_list.append(Subject(name="Operating Systems 2", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Artificial Intelligence Fundamentals", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Physics", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Introduction to Computer Science", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computer Network Administration", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Network Programming", semester=6, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    # 7th semester - field_of_study1
    subject_list.append(Subject(name="Artificial Intelligence", semester=7, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Final Project Seminar", semester=7, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Industrial Placement", semester=7, fieldOfStudy=field_of_study1))
    subject_list.append(Subject(name="Intellectual Property Protection", semester=7, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Health and Safety", semester=7, fieldOfStudy=field_of_study1,lecture_hours=30, laboratory_hours=30))
    # 1st semester - field_of_study2
    subject_list.append(Subject(name="Database Servers", semester=1, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computing Methods and Optimization", semester=1, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Advanced Object Programming in Java",semester=1,fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Modelling and Analysis of Information Systems",semester=1, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Problem Based Workshop",semester=1,fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Database Administration",semester=1,fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    # 2nd semester - field_of_study2
    subject_list.append(Subject(name="Mathematical Linguistics", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Effective Java Programming", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Compiler Construction", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Advanced Networking Technology", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Computational Intelligence", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Economics, Management and Law", semester=2, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    # 3rd semester - field_of_study2
    subject_list.append(Subject(name="Scientific Computing", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Recent Advances in Computer Science", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Final Project Seminar", semester=3, fieldOfStudy=field_of_study2))
    subject_list.append(Subject(name="Cloud Architecture and Virtualisation", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))
    subject_list.append(Subject(name="Final Project", semester=3, fieldOfStudy=field_of_study2))
    subject_list.append(Subject(name="User Interface Programming", semester=3, fieldOfStudy=field_of_study2,lecture_hours=30, laboratory_hours=30))

    for sub in subject_list:
        sub.save()

    plan_list = []
    plan_list.append(Plan(title=""))