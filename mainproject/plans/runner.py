import traceback
from multiprocessing import Pool
from entities.models import Teacher, Room, FieldOfStudy, Plan, ScheduledSubject
from .algorithm import OnePlanGenerator

def run_it_in_shell():
    cpm = CreatePlanManager()
    cpm.create_plan_asynch(winterOrSummer=FieldOfStudy.SUMMER, how_many_plans=2)
    cpm.save_the_best_result()


class CreatePlanManager():
    def __init__(self):
        self.results = []

    def create_plan(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3, teachers=None, rooms=None, fields_of_study=None,
                    min_hour=8, max_hour=19):
        # teachers = Teacher.objects.all()
        # rooms = Room.objects.all()
        # fields_of_study = FieldOfStudy.objects.all()
        from django.db import connection
        connection.close()
        result = {"Exception"}
        try:
            plans = OnePlanGenerator.create_empty_plans(fields_of_study, how_many_plans, winterOrSummer)
            # OnePlanGenerator.show_objects(plans)
            # in test purpose only!!!
            first_plan = OnePlanGenerator(teachers, plans, rooms)
            result = first_plan.generate_plan(min_hour, max_hour)
        except Exception as e:
            print("Exception was thrown")
            print(str(e))
            print(e.__class__)
            print(e.__cause__)
        return result

    def create_plans_without_deleting_plans(self):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        plans = list(Plan.objects.all())
        for plan in plans:
            plan.id = None
        result = {"Exception"}
        try:
            # OnePlanGenerator.show_objects(plans)
            # in test purpose only!!!
            first_plan = OnePlanGenerator(teachers, plans, rooms)
            result = first_plan.generate_plan()
        except:
            print("Exception was thrown")
        return result

    def create_plan_asynch(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3, min_hour=8, max_hour=19):
        pool = Pool(processes = 4)
        list_with_arguments = []
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields_of_study = FieldOfStudy.objects.all()
        for i in range(10):
            list_with_arguments.append((winterOrSummer, how_many_plans, teachers, rooms,
                                        fields_of_study, min_hour, max_hour))
        print(list_with_arguments)
        self.results = pool.starmap(self.create_plan, list_with_arguments)
        print(self.results)

    def find_the_best_result(self):
        print("----- Show results -----")
        print(self.results)
        the_best_result = None
        for result in self.results:
            print(result)
            print(len(result))
            if the_best_result and len(result) == 2:
                if the_best_result[1] > result[1]:
                    print(result)
                    the_best_result = result
            elif len(result) == 2:
                the_best_result = result
        print("The_best_result")
        print(result)
        return the_best_result

    def save_the_best_result(self):
        from django.db import connection
        connection.close()
        result_to_save = self.find_the_best_result()
        if result_to_save:
            plans = result_to_save[0].plans
            sch_subject_plans = result_to_save[0].subjects_in_plans
            ScheduledSubject.objects.all().delete()
            Plan.objects.all().delete()
            print("plans:")
            # for plan in Plan.objects.all():
            #     plan.delete()
            for plan in Plan.objects.all():
                print(plan)
            print("subjects:")
            for sch_subject in ScheduledSubject.objects.all():
                print(sch_subject)
            # SAVE
            for plan in plans:
                plan.save()
            for i in range(len(plans)):
                title = sch_subject_plans[i][0].plan.title
                plan = Plan.objects.get(title=title)
                print(plan)
                print(plans[i])
                for sch_subject in sch_subject_plans[i]:
                    sch_subject.plan = plan
                    sch_subject.save()

