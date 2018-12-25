from numpy import array, nditer, zeros
from random import randint

class ImprovementManager:

    def __init__(self, plans, subjects):
        self.day_of_week = array([1, 2, 3, 4, 5, 6, 7])
        self.data = zeros(shape=(len(plans),self.day_of_week.size), dtype=object)
        plan_ids_list = []
        row = 0
        for p in plans:
            plan_ids_list.append(p.id)
            scheduled_subjects = subjects.filter(plan=p)
            for i in range(1, 8):  # 1 2 3 4 5 6 7
                self.data[row][i-1] = list(scheduled_subjects.filter(dayOfWeek=i))
            row = row + 1
        self.plans_ids = array(plan_ids_list)

    def generation(self):
        number_of_plans = self.plans_ids.size
        which_plan_will_be_mutated = randint(0,number_of_plans)
        # for i in range(0,number_of_plans):
        buff = self.data[which_plan_will_be_mutated]
        print("+++ ONE PLAN +++")
        print(self.plans_ids[which_plan_will_be_mutated])
        print(buff)
        for list_sch in buff:
            print(list_sch)

    def repair_generation(self):
        pass

    def value_for_plan(self, plan):
        pass

    def check_subject_to_subjects(self):
        pass

    def check_subject_to_teacher_time(self):
        pass

    def check_subject_to_rooms(self):
        pass

    def make_improvement(self, number_of_generation):
        pass

    def pass_to_database(self):
        pass

    def show_data(self):
        print(self.plans_ids)
        print(self.data)
