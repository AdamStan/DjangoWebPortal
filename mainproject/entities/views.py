from django.shortcuts import render
import json
class SubjectExample:
    name = ""
    when_started = 0
    how_long = 0
    day = "monday"
    def toJSON(self):
        return json.dumps(self.__dict__)

def create_table():
    values = []
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    subject1 = SubjectExample()
    subject1.name = "Subject1"
    subject1.when_started = 9
    subject1.how_long = 2
    subject1.day = 'monday'

    print(subject1.toJSON())
    values.append(subject1.toJSON())

    subject2 = SubjectExample()
    subject2.name = "Subject2"
    subject2.when_started = 11
    subject2.how_long = 2
    subject2.day = 'tuesday'

    values.append(subject2.toJSON())

    subject3 = SubjectExample()
    subject3.name = "Subject3"
    subject3.when_started = 13
    subject3.how_long = 2
    subject3.day = 'wednesday'

    values.append(subject3.toJSON())

    subject4 = SubjectExample()
    subject4.name = "Subject4"
    subject4.when_started = 15
    subject4.how_long = 2
    subject4.day = 'thursday'

    values.append(subject4.toJSON())

    subject5 = SubjectExample()
    subject5.name = "Subject5"
    subject5.when_started = 17
    subject5.how_long = 2
    subject5.day = 'friday'

    values.append(subject5.toJSON())

    return {'values': values}

def show_timetables(request):
    parameters = create_table()
    return render(request, 'admin/timetables.html', parameters);

def show_student_plans(request):
    parameters = create_table()
    pass

def show_teacher_plan(request):
    parameters = create_table()
    pass