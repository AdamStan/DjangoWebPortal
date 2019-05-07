from multiprocessing import Process, Pool
from entities.models import Teacher, Room, FieldOfStudy, Plan
from .algorithm import OnePlanGenerator
from itertools import product
from functools import partial
from itertools import repeat

def run_it_in_shell():
    cpm = CreatePlanManager()
    cpm.create_plan_asynch()
    cpm.save_the_best_result()


class CreatePlanManager():
    def __init__(self):
        self.results = []

    def create_plan(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3):
        teachers = Teacher.objects.all()
        rooms = Room.objects.all()
        fields_of_study = FieldOfStudy.objects.all()
        result = {"Exception"}
        try:
            plans = OnePlanGenerator.create_empty_plans(fields_of_study, how_many_plans, winterOrSummer)
            # OnePlanGenerator.show_objects(plans)
            # in test purpose only!!!
            first_plan = OnePlanGenerator(teachers, plans, rooms)
            result = first_plan.generate_plan()
        except:
            print("Exception was thrown")
        return result

    def create_plans_without_deleting_plans(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3):
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

    def create_plan_asynch(self, winterOrSummer=FieldOfStudy.WINTER, how_many_plans=3):
        # p1=Process(target=run_it_in_shell)
        # p2=Process(target=run_it_in_shell)
        # p3=Process(target=run_it_in_shell)
        # processes = []
        # result = []
        # for i in range(10):
        #     processes.append(Process(target=run_it_in_shell()))
        #     processes[-1].start()
        #
        # for process in processes:
        #     process.join()
        pool = Pool(processes = 4)
        # self.results = pool.map(self.create_plan, product(winterOrSummer, how_many_plans, repeat=10))
        list_with_arguments = []
        for i in range(10):
            list_with_arguments.append((winterOrSummer, how_many_plans))
        print(list_with_arguments)
        self.results = pool.starmap(self.create_plan, list_with_arguments)
        print(self.results)

    def find_the_best_result(self):
        the_best_result = None
        for result in self.results:
            if len(result) > 1 and the_best_result:
                if the_best_result[1] > result[1]:
                    the_best_result = result
            else:
                the_best_result = result
        return the_best_result

    def save_the_best_result(self):
        result_to_save = self.find_the_best_result()
        if result_to_save:
            result_to_save[0].save_result()

