from entities.models import Subject, ScheduledSubject, Teacher, Plan, Room, FieldOfStudy
from random import randint, choice
import threading
import multiprocessing as mp
from datetime import time

# :::STATIC VALUES:::
HOW_MANY_TRIES = 100

''' 
It will be request function:
'''
def run_it_in_shell(winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3):
    teachers = Teacher.objects.all()
    rooms = Room.objects.all()
    fields_of_study = FieldOfStudy.objects.all()

    plans = OnePlanGenerator.create_empty_plans(fields_of_study, how_many_plans, winterOrSummer)

    show_objects(plans)
    # in test purpose only!!!
    OnePlanGenerator(teachers, plans, rooms).generate_plan()


def show_objects(objects):
    for obj in objects:
        print(str(obj))

def show_subjects(scheduled_subjects):
    for sch in scheduled_subjects:
        print(str(sch) + ", " + str(sch.whenStart) + ", " + str(sch.whenFinnish) + ", day:" + str(sch.dayOfWeek)
              + ", how_long: " + str(sch.how_long))

class OnePlanGenerator:
    def __init__(self, teachers, plans, rooms, weeks=15):
        self.teachers = list(teachers)
        self.plans = plans
        self.rooms = list(rooms)
        # there will be the same index as in plans, teachers, rooms
        self.subjects_in_plans = []
        self.subjects_for_teachers = []
        self.subjects_in_room = []

        for plan in self.plans:
            scheduled_subjects = OnePlanGenerator.create_scheduled_subjects(plan, weeks)
            self.subjects_in_plans.append(scheduled_subjects)

        for room in self.rooms:
            self.subjects_in_room.append([])

        for teacher in self.teachers:
            self.subjects_for_teachers.append([])

    @staticmethod
    def create_empty_plans(fields_of_study, how_many_plans, winter_or_summer):
        plans = []

        for field in fields_of_study:
            if field.whenDoesItStarts == winter_or_summer:
                sm = 1
            else:
                sm = 2
            for sem in range(sm, field.howManySemesters + 1, 2):
                for i in range(1, how_many_plans + 1):
                    plans.append(Plan(title=field.name + str(sem) + "_" + str(i), fieldOfStudy=field, semester=sem))
        return plans

    @staticmethod
    def create_scheduled_subjects(plan, weeks):
        subjects = Subject.objects.filter(fieldOfStudy=plan.fieldOfStudy, semester=plan.semester)
        list_of_scheduled_subjects = []
        for subject in subjects:
            if subject.lecture_hours and subject.lecture_hours > 0:
                list_of_scheduled_subjects.append(
                    ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LECTURE,
                                     how_long=int(subject.lecture_hours / weeks))
                )
            if subject.laboratory_hours and subject.laboratory_hours > 0:
                list_of_scheduled_subjects.append(
                    ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LABORATORY,
                                     how_long=int(subject.laboratory_hours / weeks))
                )
        return list_of_scheduled_subjects

    def generate_plan(self, min_hour=8, max_hour=19, days=[1,2,3,4,5]):
        """
        Creates timetable first time
        :param scheduled_subjects: subjects without schedule
        :param min_hour: first hour when subject can start
        :param max_hour: last hour when subject can start
        :param days: days in week 0 => sunday, 6=> saturday
        :param weeks: how many weeks semester can be
        :return: None
        """
        self.set_lectures_time(min_hour=min_hour, max_hour=max_hour, days=days)
        self.set_laboratory_time(min_hour=min_hour, max_hour=max_hour, days=days)
        self.set_rooms_to_subjects()
        self.set_teachers_to_class()

    def set_lectures_time(self, min_hour=8, max_hour=19, days=[1,2,3,4,5]):
        """
        Randomizes days of week and hours when lectures will take place
        :param scheduled_subjects: subjects without schedule
        :param min_hour: first hour when subject can start
        :param max_hour: last hour when subject can start
        :param days: days in week 0 => sunday, 6=> saturday
        :param weeks: how many weeks semester can be
        :return None:
        """
        dict_lectures = {}
        for list_index in range(0, len(self.subjects_in_plans)):
            for subject_index in range(len(self.subjects_in_plans[list_index])):
                if self.subjects_in_plans[list_index][subject_index].type == ScheduledSubject.LECTURE:
                    new_id = str(list_index) + "|||" + str(subject_index)
                    dict_lectures[new_id] = self.subjects_in_plans[list_index][subject_index]

        print("--- set lectures time ---")
        dict_group_lectures = {}

        for sch_subject in dict_lectures.values():
            dict_group_lectures[sch_subject.subject] = []

        print(dict_group_lectures.__len__())
        print(dict_lectures.__len__())

        for sch_subject in dict_lectures.values():
            dict_group_lectures[sch_subject.subject].append(sch_subject)

        for sch_subject_list in dict_group_lectures.values():
            tries = HOW_MANY_TRIES
            while tries > 0:
                when_start = randint(min_hour, max_hour)
                which_day = choice(days)
                sch_subject_list[0].whenStart = time(when_start, 0, 0)
                sch_subject_list[0].dayOfWeek = which_day
                sch_subject_list[0].whenFinnish = time(when_start + sch_subject_list[0].how_long, 0, 0)
                check_for_this_key = ""
                for key, value in dict_lectures.items():
                    if value == sch_subject_list[0]:
                        check_for_this_key = key
                        break
                if self.check_event_can_be_set(event=sch_subject_list[0], event_id=check_for_this_key, dict_of_subjects=dict_lectures):
                    for sch_subject in sch_subject_list:
                        sch_subject.whenStart = time(when_start, 0, 0)
                        sch_subject.dayOfWeek = which_day
                        sch_subject.whenFinnish = time(when_start + sch_subject_list[0].how_long, 0, 0)
                    break
            tries -= 1
            if tries == 0:
                raise Exception("lectures cannot be set!")

        show_subjects(dict_lectures.values())

    def set_laboratory_time(self, min_hour=8, max_hour=19, days=[1,2,3,4,5]):
        """
        Randomizes days of week and hours when lectures will take place
        :param scheduled_subjects: subjects without schedule
        :param min_hour: first hour when subject can start
        :param max_hour: last hour when subject can start
        :param days: days in week 0 => sunday, 6=> saturday
        :param weeks: how many weeks semester can be
        :return None:
        """
        # dictionary for all laboratories
        dict_laboratories = {}
        for list_index in range(0, len(self.subjects_in_plans)):
            for subject_index in range(len(self.subjects_in_plans[list_index])):
                if self.subjects_in_plans[list_index][subject_index].type == ScheduledSubject.LABORATORY:
                    new_id = str(list_index) + "|||" + str(subject_index)
                    dict_laboratories[new_id] = self.subjects_in_plans[list_index][subject_index]

        # dictionary for all events
        dict_all = {}
        for list_index in range(0, len(self.subjects_in_plans)):
            for subject_index in range(len(self.subjects_in_plans[list_index])):
                new_id = str(list_index) + "|||" + str(subject_index)
                dict_all[new_id] = self.subjects_in_plans[list_index][subject_index]

        print("--- set laboratories time ---")
        for key, subject in dict_laboratories.items():
            tries = HOW_MANY_TRIES
            while tries > 0:
                when_start = randint(min_hour, max_hour)
                which_day = choice(days)
                subject.whenStart = time(when_start, 0, 0)
                subject.dayOfWeek = which_day
                subject.whenFinnish = time(when_start + subject.how_long, 0, 0)
                tries -= 1
                if self.check_event_can_be_set(event=subject, event_id=key, dict_of_subjects=dict_all):
                    break
                if tries == 0:
                    raise Exception("Laboratories cannot be set!")

        show_subjects(dict_laboratories.values())

    def set_rooms_to_subjects(self):
        self.set_rooms_for_lectures()
        self.set_rooms_for_laboratories()

    def set_rooms_for_lectures(self):
        pass

    def set_rooms_for_laboratories(self):
        pass

    def set_teachers_to_class(self):
        self.teachers_to_lectures()
        self.teachers_to_labs()

    def teachers_to_lectures(self):
        pass

    def teachers_to_labs(self):
        pass

    def check_teacher_can_teach(self, teacher):
        pass

    def check_room_can_be_set(self, room):
        pass

    def check_event_can_be_set(self, event, event_id, dict_of_subjects):
        # search the subject from plan
        for key, value in dict_of_subjects.items():
            if event_id[0:3] == key[0:3] and event_id != key:
                try:
                    difference_between_starts = abs(event.whenStart.hour - dict_of_subjects[key].whenStart.hour)
                    difference_between_ends = abs(event.whenFinnish.hour - dict_of_subjects[key].whenFinnish.hour)
                    is_the_same_day = event.dayOfWeek == dict_of_subjects[key].dayOfWeek
                    # show_subjects([value])
                    # show_subjects([event])
                    if is_the_same_day and \
                            difference_between_starts + difference_between_ends <= event.how_long + dict_of_subjects[key].how_long:
                        print("I return false")
                        return False
                except AttributeError:
                    return True
        return True

    def show(self):
        for events in self.subjects_in_plans.values():
            print("+++------------+++")
            for event in events:
                print(event)


class GeneratorPlans:
    def __init__(self):
        self.plans_generators = {}

    # https://stackabuse.com/parallel-processing-in-python/ check
    def generate_plans(self, teachers=None, plans=None, rooms=None, events=None, how_many=3):
        tasks = []
        list_of_plans = []
        for i in range(0,how_many):
            # plans = OnePlanGenerator(teachers, plans, rooms, events)
            tasks.append(threading.Thread(target=self.write(i)))

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

        # async example, basic
        # more: https://realpython.com/asynchronous-tasks-with-django-and-celery/
        # and: http://www.celeryproject.org
        with mp.Pool(processes=how_many) as pool:
            multiple_results = [pool.apply_async(func=self.write) for i in range(4)]

            print(multiple_results.__len__())
            res = pool.apply_async(time.sleep, (10,))

            try:
                print(res.get(timeout=1))
            except TimeoutError:
                print("We lacked patience and got a multiprocessing.TimeoutError")

    def write(self, para):
        for i in range(0,100):
            print(str(para) + str(i))
        return para