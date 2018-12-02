from .models import ScheduledSubject, Plan
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

def clean_plans():
    pass
def clean_scheduled_subjects(subjects):
    pass

def create_scheduled_subjects(subjects):
    pass

def create_first_plan(scheduled_subjects, min_hour=8, max_hour=19, days=[1,2,3,4,5], weeks = 15):
    for s in scheduled_subjects:

        if s.type == "LAB":
            s.how_long = int(s.subject.laboratory_hours / weeks)
        elif s.type == "LEC":
            s.how_long = int(s.subject.lecture_hours / weeks)

        when_start = randint(min_hour,max_hour)
        which_day = choice(days)
        s.whenStart = time(when_start,0,0)
        s.dayOfWeek = which_day
        s.whenFinnish = time(when_start + s.how_long,0,0)

        s.save()

def generation():
    pass

def repair_generation():
    pass

@transaction.atomic
def create_plans():
    sid = transaction.savepoint()
    # in this moment we have to create plans
    try:
        scheduled_subject_qs = ScheduledSubject.objects
        clean_scheduled_subjects(scheduled_subject_qs)
        plans = Plan.objects.all()

        for p in plans:
            temp_subject_list = scheduled_subject_qs.filter(plan=p)
            # show_scheduled_subject(temp_subject_list)
            create_first_plan(temp_subject_list)

        transaction.savepoint_commit(sid)

    except Exception as e:
        transaction.savepoint_rollback(sid)
        print(str(e))

def show_scheduled_subject(scheduled_subjects):
    for ss in scheduled_subjects:
        print("Subject's name: " + ss.subject.name)
        print("When started: " + str(ss.whenStart))
        print("Which day: " + str(ss.dayOfWeek))
        print("Plan: " + ss.plan.title)
        print("How long: " + str(ss.how_long))
