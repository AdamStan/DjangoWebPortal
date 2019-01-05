from django.shortcuts import render
from accounts.models import User
from .models import *
from .algorithm import create_plans


class SubjectExample:
    id = 0
    name = ""
    whenStart = 0
    how_long = 0
    day = "monday"
    def toJSON(self):
        return json.dumps(self.__dict__)


class TeacherBox:
    id = 0
    title = ""


def create_table_example():
    values = []

    subject1 = SubjectExample()
    subject1.id = 1
    subject1.name = "Subject1"
    subject1.whenStart = 9
    subject1.how_long = 2
    subject1.day = 'monday'

    print(subject1.toJSON())
    values.append(subject1.toJSON())

    subject2 = SubjectExample()
    subject2.id = 2
    subject2.name = "Subject2"
    subject2.whenStart = 11
    subject2.how_long = 2
    subject2.day = 'tuesday'

    values.append(subject2.toJSON())

    subject3 = SubjectExample()
    subject3.id = 3
    subject3.name = "Subject3"
    subject3.whenStart = 13
    subject3.how_long = 2
    subject3.day = 'wednesday'

    values.append(subject3.toJSON())

    subject4 = SubjectExample()
    subject4.id = 4
    subject4.name = "Subject4"
    subject4.whenStart = 15
    subject4.how_long = 2
    subject4.day = 'thursday'

    values.append(subject4.toJSON())

    subject5 = SubjectExample()
    subject5.id = 5
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
    subjects = ScheduledSubject.objects.filter(plan=plan).order_by('dayOfWeek')
    values = []
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday",]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        teacher_name = ss.teacher.user.name + " " + ss.teacher.user.surname
        buff.name = ss.subject.name + " " + ss.type + " " + teacher_name
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, plan.title

def get_teachers():
    teacher = Teacher.objects.all()
    return teacher

def create_table_for_teacher(teacher_id):
    teacher = Teacher.objects.get(user_id=teacher_id)
    subjects = ScheduledSubject.objects.filter(teacher=teacher).order_by('dayOfWeek')
    values = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        buff.name = ss.subject.name + " " + ss.type + " " + ss.plan.title
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, teacher.user.id

def get_plans_for_rooms():
    rooms = Room.objects.all()
    return rooms

def create_table_for_room(room_id):
    room = Room.objects.get(id=room_id)
    subjects = ScheduledSubject.objects.filter(room=room).order_by('dayOfWeek')
    values = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", ]

    for ss in subjects:
        buff = SubjectExample()
        buff.id = ss.id
        teacher_name = ss.teacher.user.name + " " + ss.teacher.user.surname
        buff.name = ss.subject.name + " " + ss.type + " " + ss.plan.title + " " + teacher_name
        buff.whenStart = ss.whenStart.hour
        buff.how_long = ss.how_long
        buff.day = days[ss.dayOfWeek-1]

        values.append(buff.toJSON())

    return {"values": values}, room.id

""" ::: VIEWS FOR ADMINS ::: """

def show_timetables(request):
    return render(request, 'admin/timetable_intro.html');

def show_student_plans(request):
    plans = get_plans()
    plan_title = ""
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        print("Which value was taken: " + value)
        parameters, plan_title = create_table(value)
    else:
        parameters = create_table_example()

    return render(request, 'admin/timetables.html', {"values": parameters['values'], "plans": plans, "plan_title":plan_title,"type":"student"});


def show_teachers_plans(request):
    teachers = get_teachers()
    plan_title = "Example"
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        print("Which value was taken: " + value)
        parameters, plan_title = create_table_for_teacher(value)
    else:
        parameters = create_table_example()

    teachers_boxes = []
    for t in teachers:
        teachers_boxes.append(TeacherBox())
        teachers_boxes[-1].id = t.user.id
        teachers_boxes[-1].title = t.user.surname + ", " + t.user.name
    return render(request, 'admin/timetables.html', {"values": parameters['values'], "plans": teachers_boxes , "plan_title":plan_title, "type": "teacher"});

def show_rooms_plans(request):
    plans = get_plans_for_rooms()
    plan_title = "Example"
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        print("Which value was taken: " + value)
        parameters, plan_title = create_table_for_room(value)
    else:
        parameters = create_table_example()
    return render(request, 'admin/timetables.html',{"values": parameters['values'], "plans": plans, "plan_title": plan_title, "type":"room"});

def show_generate_page(request):
    fail_message = ""
    s_message = ""
    if request.method == 'POST':
        min_hour = request.POST.get("first_hour")
        max_hour = request.POST.get("last_hour")
        semester_type = request.POST.get("semester_type")
        how_many_groups = request.POST.get("how_many_groups")
        if max_hour == "" or min_hour == "" or semester_type == "None" or how_many_groups == "":
            fail_message = "Plans cannot be create with this values "
        else:
            #max_hour=int(max_hour), min_hour=int(min_hour), semester=int(semester_type), number_of_groups=int(how_many_groups)
            create_plans(max_hour=int(max_hour), min_hour=int(min_hour), semester=int(semester_type), number_of_groups=int(how_many_groups))
            s_message = "Everything goes fine, check plans in AllPlans tab"

    return render(request,'admin/generate.html', {"fail_message": fail_message, "s_message":s_message } )

def show_edit_timetable(request):
    plans = get_plans()
    plan_title = ""
    if request.method == 'POST':
        value = request.POST.get('plan_id', None)
        print("Which value was taken: " + value)
        parameters, plan_title = create_table(value)
    else:
        parameters = { "values": [] }
    return render(request, 'admin/edit_timetables.html',{"values": parameters['values'], "plans": plans, "plan_title":plan_title})

""" ::: VIEWS FOR STUDENT AND TEACHER ONLY ::: """

def show_user_plan(request):
    user_id = request.user.id
    parameters, plan_title = create_table_for_teacher(25) # add user_id
    print(parameters)
    return render(request, 'teacher/myplan.html', { "values": parameters['values'], "plan_title": plan_title })

def show_choose_plan(request):
    # student_id = request.user.id
    # student = Student.objects.get(id=student_id) # add student id
    # plans = Plan.objects.filter(fieldOfStudy = student.fieldOfStudy, semester = student.semester)
    temp_field = FieldOfStudy.objects.get(id=7)
    plans = Plan.objects.filter(fieldOfStudy=temp_field, semester=1)
    plan_id = plans.first().id
    parameters, plan_title = create_table(plans.first().id)

    message = ""
    if request.POST:
        action = request.POST.get('action_name', None)
        print(action)
        if action == "search":
            plan_id = request.POST.get('plan_id', None)
            print("show plan " + str(plan_id))
            parameters, plan_title = create_table(plan_id)
        elif action == "add":
            plan_id = request.POST.get('which_plan', None)
            print("add student")
            parameters, plan_title = create_table(plan_id)
            student_buff = Student.objects.get(user_id=15)
            student_buff.plan = plans.get(id=plan_id)
            student_buff.save()
            message = "You were added to this plan"
        elif action == "delete":
            print("delete student")
            student_buff = Student.objects.get(user_id=15)
            student_buff.plan = None
            student_buff.save()
            message = "You were deleted from your plan, now you don't have a group"

    print(parameters)
    return render(request, 'student/myplans.html',
                  {"values": parameters['values'], "plans": plans, "plan_title": plan_title, "which_plan": plan_id, "message": message});
