from django.shortcuts import render
import json
from .models import *
from django.forms.models import model_to_dict
from datetime import time

class SubjectExample:
    id = 0
    name = ""
    whenStart = 0
    how_long = 0
    day = "monday"
    def toJSON(self):
        return json.dumps(self.__dict__)

def create_table_example():
    values = []

    subject1 = SubjectExample()
    subject1.name = "Subject1"
    subject1.whenStart = 9
    subject1.how_long = 2
    subject1.day = 'monday'

    print(subject1.toJSON())
    values.append(subject1.toJSON())

    subject2 = SubjectExample()
    subject2.name = "Subject2"
    subject2.whenStart = 11
    subject2.how_long = 2
    subject2.day = 'tuesday'

    values.append(subject2.toJSON())

    subject3 = SubjectExample()
    subject3.name = "Subject3"
    subject3.whenStart = 13
    subject3.how_long = 2
    subject3.day = 'wednesday'

    values.append(subject3.toJSON())

    subject4 = SubjectExample()
    subject4.name = "Subject4"
    subject4.whenStart = 15
    subject4.how_long = 2
    subject4.day = 'thursday'

    values.append(subject4.toJSON())

    subject5 = SubjectExample()
    subject5.name = "Subject5"
    subject5.whenStart = 17
    subject5.how_long = 2
    subject5.day = 'friday'

    values.append(subject5.toJSON())

    return {'values': values}

def get_plans():
    plans = Plan.objects.all()
    return plans

def create_table(plan_id):
    plan = Plan.objects.get(id=plan_id)
    subjects = ScheduledSubject.objects.filter(plan=plan)
    values = []
    days = [
        "monday",
        "tuseday",
        "wenesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        buff.name = ss.subject.name + " " + ss.type
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek]

        values.append(buff.toJSON())

    return {"values": values}

def get_plan_for_teacher():
    pass

def get_plans_for_rooms():
    pass

def show_timetables(request):
    return render(request, 'admin/timetable_intro.html');

def show_student_plans(request):
    plans = get_plans()
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        print("Which value was taken: " + value)
        parameters = create_table(value)
    else:
        parameters = create_table_example()

    return render(request, 'admin/timetables.html', {"values": parameters['values'], "plans": plans, });

def show_teacher_plan(request):
    parameters = create_table()
    pass