from .models import ScheduledSubject, Plan
import random
'''
For every Scheduled Subject we have to add single teacher
    We get this teacher from subject.teachers.
We have to choose a day and hour when it begins
How_long will be calculated from lecture_hours/laboratory
We will have to put as parameter, date for first day of teaching
We also have to choose rooms, I know how to do it, but I am so scary about it
'''
def create_first_plan(scheduled_subjects, min_hour=8, max_hour=19, days=[1,2,3,4,5]):

    for s in scheduled_subjects:
        print(random(min_hour,max_hour))
        print(random.choices(days))

def generation():
    pass

def repair_generation():
    pass

def create_plans():
    scheduled_subject_qs = ScheduledSubject.objects
    plans = Plan.objects.all()

    for p in plans:
        temp_subject_list = scheduled_subject_qs.filter(plan=p)
        show_scheduled_subject(temp_subject_list)
        create_first_plan(temp_subject_list)
        break

def show_scheduled_subject(scheduled_subjects):
    for ss in scheduled_subjects:
        print("Subject's name: " + ss.subject.name)
        print("When started: " + str(ss.whenStart))
        print("Plan: " + ss.plan.title)