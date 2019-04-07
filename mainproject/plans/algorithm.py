from entities.models import Subject, ScheduledSubject, Teacher, Plan, Room, FieldOfStudy
import threading
import multiprocessing as mp
import time

def run_it_in_shell(winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    rooms = Room.objects.all()
    fields_of_study = FieldOfStudy.objects.all()

    plans = []
    OnePlanGenerator.create_plans(fields_of_study, how_many_plans, winterOrSummer)

    show_objects(plans)

    OnePlanGenerator(teachers, plans, rooms, )


def show_objects(objects):
    for obj in objects:
        print(str(obj))


class OnePlanGenerator:
    def __init__(self, teachers, plans, rooms, events):
        self.dict_of_teachers = {}
        self.dict_of_plans = {}
        self.dict_of_rooms = {}

        for teacher in teachers:
            self.dict_of_teachers[teacher] = []

        for plan in plans:
            scheduled_subjects = Plans.create_scheduled_subjects(plan)
            self.dict_of_plans[plan] = [scheduled_subjects]

        for room in rooms:
            self.dict_of_rooms[room] = []

        self.list_of_events = events

    @staticmethod
    def create_plans(fields_of_study, how_many_plans):
        plans = []
        for field in fields_of_study:
            for sem in range(1, field.howManySemesters + 1):
                for i in range(1, how_many_plans + 1):
                    plans.append(Plan(title=field.name + str(sem) + "_" + str(i), fieldOfStudy=field, semester=sem))
        return plans

    @staticmethod
    def create_scheduled_subjects(plan):
        subjects = Subject.objects.filter(fieldOfStudy=plan.fieldOfStudy, semester=plan.semester)
        list_of_scheduled_subjects = []
        for subject in subjects:
            if subject.lecture_hours and subject.lecture_hours > 0:
                list_of_scheduled_subjects.append(
                    ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LECTURE)
                )
            if subject.laboratory_hours and subject.laboratory_hours > 0:
                list_of_scheduled_subjects.append(
                    ScheduledSubject(subject=subject, plan=plan, type=ScheduledSubject.LABORATORY)
                )
        return list_of_scheduled_subjects

    def generate_plan(self):
        OnePlanGenerator.create_scheduled_subjects()

    def check_teacher_can_teach(self, teacher):
        pass

    def check_room_can_be_set(self, room):
        pass

    def check_event_can_be_set(self, event):
        pass

    def show(self):
        for events in self.dict_of_plans.values():
            print("+++------------+++")
            for event in events:
                print(event)


class Plans:
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