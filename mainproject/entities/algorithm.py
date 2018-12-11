from .models import ScheduledSubject, Plan, FieldOfStudy, Subject
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
    bachelor_semesters = [1, 2, 3, 4, 6, 7]
    master_semesters = [1, 2, 3]
    only_master_semesters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def clean_plans():
    clean_scheduled_subjects_all()
    Plan.objects.all().delete()

def clean_scheduled_subjects_all():
    ScheduledSubject.objects.all().delete()

def create_skeleton(how_many=3,semester=1):
    field_of_studies = FieldOfStudy

def create_first_plan(scheduled_subjects, min_hour=8, max_hour=19, days=[1,2,3,4,5], weeks = 15):
    clean_plans()

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
        clean_scheduled_subjects_all(scheduled_subject_qs)
        plans = Plan.objects.all()

        # create new skeleton

        # create first plan

        for p in plans:
            temp_subject_list = scheduled_subject_qs.filter(plan=p)
            # show_scheduled_subject(temp_subject_list)
            create_first_plan(temp_subject_list)

        transaction.savepoint_commit(sid)
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print(str(e))

    # make_improvemnets()

def create_skeleton(number_of_group = 3, semester = 1):
    fields_of_study = FieldOfStudy.objects.all()

    filter_list = filter(lambda x : x % 2 == semester, AlgorithmManager.only_master_semesters)
    print("e:" + str(filter_list))
    print("ee:" + str(fields_of_study))

    for field in fields_of_study:
        for sem in filter_list:
            try:
                subjects_for_field = Subject.objects.filter(fieldOfStudy=field).filter(semester=sem)
                print("eee: " + str(subjects_for_field))
            except:
                break
            for i in range(number_of_group):
                title = field.name + "|" + str(field.degree) + "|s" + str(sem) + "|" + str(i)
                p = Plan(title=title, fieldOfStudy=field, semester=sem)
                p.save()
                for sub in subjects_for_field:
                    if sub.lecture_hours != None and sub.lecture_hours > 0:
                        ScheduledSubject(subject=sub, plan=p, type=ScheduledSubject.LECTURE).save()
                    if sub.laboratory_hours != None and sub.laboratory_hours > 0:
                        ScheduledSubject(subject=sub, plan=p, type=ScheduledSubject.LABORATORY).save()

def show_scheduled_subject(scheduled_subjects):
    for ss in scheduled_subjects:
        print("Subject's name: " + ss.subject.name)
        print("When started: " + str(ss.whenStart))
        print("Which day: " + str(ss.dayOfWeek))
        print("Plan: " + ss.plan.title)
        print("How long: " + str(ss.how_long))
