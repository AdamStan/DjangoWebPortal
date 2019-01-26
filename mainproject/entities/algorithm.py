from .models import ScheduledSubject, Plan, FieldOfStudy, Subject, Room, Teacher, Student
from random import randint, choice
from datetime import time
from django.db import transaction
'''
For every Scheduled Subject we have to add single teacher
    We get this teacher from subject.teachers.
We have to choose a day and hour when it begins
How_long will be calculated from lecture_hours/laboratory
We will have to put as parameter, date for first day of teaching
We also have to choose rooms, I know how to do it, but I am so scary about it
3 functions:
check it can be with other subjects in plans <- FIRST, not done yet
check it can be with other teacher's subjects
check it can be with other room's subjects
'''

class AlgorithmManager:
    bachelor_semesters = [1, 2, 3, 4, 5, 6, 7]
    master_semesters = [1, 2, 3]
    only_master_semesters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plans_classification = []

def create_skeleton(number_of_group = 3, semester = 1):
    """ Creates plans with empty (without hours) scheduled_subjects
    :param number_of_group: how many groups will be created for every semester
    :param semester: 1 => 1,3,5,7,9, 0 => 2,4,6,8,10
    :return: None
    How does it work?
    1. Clean existing plans
    2. Get all fields of study
    3. Create plans for semesters from field of study
    """
    clean_plans()
    fields_of_study = FieldOfStudy.objects.all()

    filter_lambda = filter(lambda x : x % 2 == semester, AlgorithmManager.only_master_semesters)
    semesters_list = list(filter_lambda)

    for field in fields_of_study:
        for sem in semesters_list:
            if sem > field.howManySemesters:
                break
            try:
                subjects_for_field = Subject.objects.filter(fieldOfStudy=field).filter(semester=sem)
            except Exception as ex:
                str(ex)
                break
            for i in range(number_of_group):
                title = field.name + "|" + str(field.degree) + "|s" + str(sem) + "|" + str(i+1)
                p = Plan(title=title, fieldOfStudy=field, semester=sem)
                p.save()
                for sub in subjects_for_field:
                    if sub.lecture_hours != None and sub.lecture_hours > 0:
                        ScheduledSubject(subject=sub, plan=p, type=ScheduledSubject.LECTURE).save()
                    if sub.laboratory_hours != None and sub.laboratory_hours > 0:
                        ScheduledSubject(subject=sub, plan=p, type=ScheduledSubject.LABORATORY).save()

def clean_plans():
    """
    Cleans all scheduled_subjects and plans from database
    :return: None
    """
    for student in Student.objects.all():
        student.plan = None
        student.save()
    clean_scheduled_subjects_all()
    Plan.objects.all().delete()

def clean_scheduled_subjects_all():
    """
    Cleans all cheduled_subjects from database
    :return: None
    """
    ScheduledSubject.objects.all().delete()

def bullshit(s):
    s.save()

def set_lectures_time(min_hour, max_hour, days, weeks):
    lectures = ScheduledSubject.objects.filter(type="LEC")
    for s in lectures:
        flag = True
        diff_lectures = ScheduledSubject.objects.filter(subject=s.subject, type=s.type).order_by("id")
        list_lectures = []
        for slecture in diff_lectures:
            list_lectures.append(slecture)

        s.how_long = int(s.subject.lecture_hours / weeks)
        # print("::LECTURES::")
        # show_scheduled_subjects(list_lectures)
        i = search_first_not_null_hour(list_lectures)
        # print(i)
        if i is not None:
            s.dayOfWeek = list_lectures[i].dayOfWeek
            s.whenStart = list_lectures[i].whenStart
            s.whenFinnish = list_lectures[i].whenFinnish
            s.teacher = list_lectures[i].teacher
            s.save()
            flag = False

        scheduled_subjects_in_plan = ScheduledSubject.objects.filter(plan=s.plan).order_by("plan__id")
        while flag:
            try:
                when_start = randint(min_hour, max_hour)
                which_day = choice(days)
                s.whenStart = time(when_start, 0, 0)
                s.dayOfWeek = which_day
                s.whenFinnish = time(when_start + s.how_long, 0, 0)
                if check_subject_to_subject_time(s, scheduled_subjects_in_plan):
                    s.save()
                    set_teacher_to_subjects(s)
                    break
            except:
                continue

def set_laboratory_time(min_hour, max_hour, days, weeks):
    laboratories = ScheduledSubject.objects.filter(type="LAB")
    for s in laboratories:
        s.how_long = int(s.subject.laboratory_hours / weeks)
        scheduled_subjects_in_plan = ScheduledSubject.objects.filter(plan=s.plan)
        while True:
            try:
                when_start = randint(min_hour, max_hour)
                which_day = choice(days)
                s.whenStart = time(when_start, 0, 0)
                s.dayOfWeek = which_day
                s.whenFinnish = time(when_start + s.how_long, 0, 0)
                if check_subject_to_subject_time(s, scheduled_subjects_in_plan):
                    s.save()
                    set_teacher_to_subjects(s)
                    break
            except:
                continue

def create_first_plan(min_hour=8, max_hour=19, days=[1,2,3,4,5], weeks = 15):
    """
    Creates timetable first time
    :param scheduled_subjects: subjects without schedule
    :param min_hour: first hour when subject can start
    :param max_hour: last hour when subject can start
    :param days: days in week 0 => sunday, 6=> saturday
    :param weeks: how many weeks semester can be
    :return: None
    """
    set_lectures_time(min_hour=min_hour, max_hour=max_hour, days=days, weeks=weeks)
    set_laboratory_time(min_hour=min_hour, max_hour=max_hour, days=days, weeks=weeks)
    set_rooms_to_subjects(ScheduledSubject.objects.all())

def check_subject_to_subject_time(sch_sub, scheduled_subjects):
    """
    Checks that subjects can start and finish on generated hour
    :param sch_sub:
    :param scheduled_subjects:
    :return: None
    """
    scheduled_subjects_in_plan = scheduled_subjects.filter(plan=sch_sub.plan)
    for scheduled in scheduled_subjects_in_plan:
        if scheduled.dayOfWeek == sch_sub.dayOfWeek and scheduled.whenStart != None:
            difference_between_starts = abs(sch_sub.whenStart.hour - scheduled.whenStart.hour)
            difference_between_ends = abs(sch_sub.whenFinnish.hour - scheduled.whenFinnish.hour)
            if difference_between_starts + difference_between_ends >= sch_sub.how_long + scheduled.how_long:
                continue
            else:
                return False
        else:
            continue
    return True

def check_subject_to_subject_time_exclude(sch_sub, scheduled_subjects):
    scheduled_subjects_in_plan = scheduled_subjects.filter(plan=sch_sub.plan).exclude(id=sch_sub.id)
    return check_subject_to_subject_time(sch_sub, scheduled_subjects_in_plan)

def set_teacher_to_subjects(s):
    teachers = s.subject.teachers.all()
    teachers_list = []
    for teacher in teachers:
        teachers_list.append(teacher)

    while len(teachers_list) > 0:
        teacher = choice(teachers_list)
        if check_teacher_can_teach(s, teacher) :
            s.teacher = teacher
            s.save()
            return
        else:
            teachers_list.remove(teacher)

    raise Exception('Properly teacher was not found for scheduled subject: ' + s.subject.name + " - " + s.type + ", from: " + s.plan.title)

def search_first_not_null_hour(lectures_list):
    i = 0
    for sub in lectures_list:
        if sub.whenStart:
            return i
        i += 1
    return None

def search_first_not_null_room(lectures_list):
    i = 0
    for sub in lectures_list:
        if sub.room:
            return i
        i += 1
    return None

def check_teacher_can_teach(scheduled_subject, teacher):
    subjects_in_plan = ScheduledSubject.objects.all().filter(teacher=teacher)
    for scheduled in subjects_in_plan:
        if scheduled.dayOfWeek == scheduled_subject.dayOfWeek:
            difference_between_starts = abs(scheduled_subject.whenStart.hour - scheduled.whenStart.hour)
            difference_between_ends = abs(scheduled_subject.whenFinnish.hour - scheduled.whenFinnish.hour)
            if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + scheduled.how_long):
                continue
            else:
                return False
        else:
            continue
    return True

def check_teacher_can_teach_exclude(scheduled_subject, teacher):
    subjects_in_plan = ScheduledSubject.objects.all().filter(teacher=teacher).exclude(id=scheduled_subject.id)
    for scheduled in subjects_in_plan:
        if scheduled.dayOfWeek == scheduled_subject.dayOfWeek:
            difference_between_starts = abs(scheduled_subject.whenStart.hour - scheduled.whenStart.hour)
            difference_between_ends = abs(scheduled_subject.whenFinnish.hour - scheduled.whenFinnish.hour)
            if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + scheduled.how_long):
                continue
            else:
                return False
        else:
            continue
    return True

def set_rooms_to_subjects(scheduled_subjects):
    all_rooms_lec = []
    all_rooms_lab = []
    for r in Room.objects.filter(room_type="LAB"):
        all_rooms_lab.append(r)

    for r in Room.objects.filter(room_type="LEC"):
        all_rooms_lec.append(r)

    for ss in scheduled_subjects:
        rooms_lab = all_rooms_lab.copy()
        rooms_lec = all_rooms_lec.copy()
        if ss.type == "LEC":
            while len(rooms_lec) > 0: # rooms is equal for this
                lectures = ScheduledSubject.objects.filter(type=ss.type, subject=ss.subject).order_by('id')
                list_lectures = []
                for slecture in lectures:
                    list_lectures.append(slecture)

                show_scheduled_subjects(list_lectures)
                i = search_first_not_null_room(list_lectures)
                print(i)
                if i is not None:
                    ss.room = list_lectures[i].room
                    ss.save()
                    break
                else:
                    room = choice(rooms_lec)
                    if check_room_is_not_taken(ss, room):
                        ss.room = room
                        ss.save()
                        break
                    else:
                        rooms_lec.remove(room)
        else:
            while len(rooms_lec) > 0:
                room = choice(rooms_lab)
                if check_room_is_not_taken(ss, room) :
                    ss.room = room
                    ss.save()
                    break
                else:
                    rooms_lab.remove(room)
        if ss.room is None:
            raise Exception('There is no properly room for: ' + ss.subject.name + ", " + ss.plan.title + ", " + ss.type)

        ss.save()


def check_room_is_not_taken(scheduled_subject, room):
    subjects_in_this_room = ScheduledSubject.objects.all().filter(room=room)
    for s in subjects_in_this_room:
        if s.dayOfWeek == scheduled_subject.dayOfWeek and scheduled_subject.whenStart != None:
            difference_between_starts = abs(scheduled_subject.whenStart.hour - s.whenStart.hour)
            difference_between_ends = abs(scheduled_subject.whenFinnish.hour - s.whenFinnish.hour)
            if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + s.how_long):
                continue
            else:
                return False
        else:
            continue
    return True

def check_room_is_not_taken_exclude(scheduled_subject, room):
    subjects_in_this_room = ScheduledSubject.objects.all().filter(room=room).exclude(id=scheduled_subject.id)
    for s in subjects_in_this_room:
        if s.dayOfWeek == scheduled_subject.dayOfWeek and scheduled_subject.whenStart != None:
            difference_between_starts = abs(scheduled_subject.whenStart.hour - s.whenStart.hour)
            difference_between_ends = abs(scheduled_subject.whenFinnish.hour - s.whenFinnish.hour)
            if (difference_between_starts + difference_between_ends) >= (scheduled_subject.how_long + s.how_long):
                continue
            else:
                return False
        else:
            continue
    return True

def check_that_plans_are_correctly(scheduled_subjects):
    # -- let's do this...
    check_room_is_not_taken()
    check_subject_to_subject_time()
    check_teacher_can_teach()

@transaction.atomic
def create_plans(number_of_groups=3, semester=1, min_hour=8, max_hour=19):
    sid = transaction.savepoint()
    # in this moment we have to create plans
    try:
        create_skeleton(number_of_group=number_of_groups, semester=semester)
        create_first_plan(min_hour=min_hour, max_hour=max_hour)

        transaction.savepoint_commit(sid)
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print(str(e))
        raise e


@transaction.atomic
def create_plans_without_delete(number_of_groups=3, semester=1, min_hour=8, max_hour=19):
    sid = transaction.savepoint()
    # in this moment we have to create plans
    try:
        clean_hours_and_teacher()
        create_first_plan(min_hour=min_hour, max_hour=max_hour)

        transaction.savepoint_commit(sid)
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print(str(e))
        raise e

def clean_hours_and_teacher():
    for ss in ScheduledSubject.objects.all():
        ss.dayOfWeek = None
        ss.whenStart = None
        ss.whenFinnish = None
        ss.teacher = None
        ss.room = None
        ss.save()


def show_scheduled_subjects(scheduled_subjects):
    for ss in scheduled_subjects:
        print(ss.subject.name + " " + str(ss.whenStart) + " " + str(ss.dayOfWeek) + " " + ss.plan.title +
              "p_id_" + str(ss.plan.id) + " " + str(ss.teacher) + " " + str(ss.room))

