from numpy import array, nditer, zeros
from random import randint, choice
from datetime import time
from copy import deepcopy

class ImprovementManager:

    def __init__(self, plans, subjects, teachers, rooms):
        self.day_of_week = array([1, 2, 3, 4, 5,]) # I've deleted 6 and 7 because we don't have saturday
        # and sunday in plans
        self.data = zeros(shape=(len(plans),self.day_of_week.size), dtype=object)
        self.data_teachers = zeros(shape=(len(teachers),self.day_of_week.size), dtype=object)
        self.data_rooms = zeros(shape=(len(rooms),self.day_of_week.size), dtype=object)

        plan_ids_list = []
        teachers_list = []
        rooms_list = []

        row = 0
        for p in plans:
            plan_ids_list.append(p.id)
            scheduled_subjects = subjects.filter(plan=p)
            for i in range(1, self.day_of_week.size + 1):  # 1 2 3 4 5 6 7
                #self.data[row][i-1] = []
                self.data[row][i-1] = list(scheduled_subjects.filter(dayOfWeek=i))
            row = row + 1

        row = 0
        for r in rooms:
            rooms_list.append(r)
            scheduled_subjects = subjects.filter(room=r)
            for i in range(1, self.day_of_week.size + 1):  # 1 2 3 4 5 6 7
                #self.data_rooms[row][i - 1] = []
                self.data_rooms[row][i - 1] = list(scheduled_subjects.filter(dayOfWeek=i))
            row = row + 1

        row = 0
        for t in teachers:
            teachers_list.append(t)
            scheduled_subjects = subjects.filter(teacher=t)
            for i in range(1, self.day_of_week.size + 1):  # 1 2 3 4 5 6 7
                #self.data_teachers[row][i - 1] = []
                self.data_teachers[row][i - 1] = list(scheduled_subjects.filter(dayOfWeek=i))
            row = row + 1


        self.plans_ids = array(plan_ids_list)
        self.teachers = array(teachers_list)
        self.rooms = array(rooms_list)

    def generation(self, min_time_start=8, max_time_start=19):
        # IMPORTANT: which_plan_will_be_mutated, which_day, which_subject_index
        number_of_plans = self.plans_ids.size
        which_plan_will_be_mutated = randint(0,number_of_plans-1)
        # for i in range(0,number_of_plans):
        buff = self.data[which_plan_will_be_mutated]
        print("+++ ONE PLAN +++")
        print(self.plans_ids[which_plan_will_be_mutated])
        print("RANDOM PLAN:")
        for list_sch in buff:
            print(list_sch)
        print("DAY:")
        which_day = choice(self.day_of_week) - 1 # because curva
        print(buff[which_day])

        if buff[which_day] == 0:
            print("Empty day was chosen")
            return
        try:
            which_subject_index = randint(0, len(buff[which_day]) - 1)
        except ValueError:
            # randint(0,0) but what if randint(0,-1)????
            which_subject_index = 0

        subject_before = buff[which_day][which_subject_index]
        subject_after = deepcopy(subject_before)
        # modification for one subject
        subject_after.dayOfWeek = choice(self.day_of_week)
        new_hour = randint(min_time_start, max_time_start)
        subject_after.whenStart = time(new_hour,0,0)
        subject_after.whenFinnish = time(new_hour + subject_after.how_long, 0, 0)

        ImprovementManager.show_subject(subject_before)
        ImprovementManager.show_subject(subject_after)

        # checks that changes don't create any conflicts
        what_return = self.check_subject_to_subjects(subject=subject_after, plan_one=buff[subject_after.dayOfWeek - 1])
        print(what_return)
        what_return = what_return and self.check_subject_to_teacher(subject=subject_after, which_day=subject_after.dayOfWeek)
        print(what_return)
        what_return = what_return and self.check_subject_to_rooms(subject=subject_after, which_day=subject_after.dayOfWeek)
        print(what_return)

        if what_return != True:
            print("SOME CASE HAVE NOT PASSED")
            return
        ### START HERE ###
        return
        # counts value for old plan
        value_before = self.value_for_plan(plan=buff)
        # count value for new plan
        new_buff = self.set_correct_subject(subject_after, which_day, which_subject_index, which_plan_will_be_mutated)
        value_after = self.value_for_plan(plan=new_buff)

        if value_after < value_before:
            self.data[which_plan_will_be_mutated] = new_buff

    def repair_generation(self):
        pass

    def value_for_plan(self, plan):
        # wzor: liczba dni niepustych + (poczotek + koniec - czas trwania przedmiotow) <- dla kazdego dnia
        pass

    def check_subject_to_subjects(self, subject, plan_one):
        for sub in plan_one:
            print("checking with: " + str(subject.dayOfWeek) + " " + str(sub.whenStart) + " " + str(sub.whenFinnish))
            difference_starts = abs(subject.whenStart.hour - sub.whenStart.hour)
            difference_ends = abs(subject.whenFinnish.hour - sub.whenFinnish.hour)
            if (difference_starts + difference_ends) >= (subject.how_long + sub.how_long) or sub.id == subject.id:
                continue
            else:
                return False
        return True

    def check_subject_to_teacher(self, subject, which_day):
        teacher_index = self.teacher_in_array(subject.teacher)
        teachers_week = self.data_teachers[teacher_index]
        teacher_day = teachers_week[which_day - 1]

        for sub in teacher_day:
            print("checking with: " + str(subject.dayOfWeek) + " " + str(sub.whenStart) + " " + str(sub.whenFinnish))
            difference_starts = abs(subject.whenStart.hour - sub.whenStart.hour)
            difference_ends = abs(subject.whenFinnish.hour - sub.whenFinnish.hour)
            if (difference_starts + difference_ends) >= (subject.how_long + sub.how_long) or sub.id == subject.id:
                continue
            else:
                return False

        return True

    def check_subject_to_rooms(self, subject, which_day):
        room_index = self.room_in_array(subject.room)
        room_week = self.data_rooms[room_index]
        room_day = room_week[which_day - 1]

        for sub in room_day:
            print("checking with: " + str(subject.dayOfWeek) + " " + str(sub.whenStart) + " " + str(sub.whenFinnish))
            difference_starts = abs(subject.whenStart.hour - sub.whenStart.hour)
            difference_ends = abs(subject.whenFinnish.hour - sub.whenFinnish.hour)
            if (difference_starts + difference_ends) >= (subject.how_long + sub.how_long) or sub.id == subject.id:
                continue
            else:
                return False
        return True

    def teacher_in_array(self, teacher):
        for i in range(0, self.teachers.size):
            if self.teachers[i] == teacher:
                return i
        return None

    def room_in_array(self, room):
        for i in range(0, self.rooms.size):
            if self.rooms[i] == room:
                return i
        return None

    def make_improvement(self, number_of_generation):
        return False

    def pass_to_database(self):
        pass

    def show_data(self):
        print(self.plans_ids)
        print("<--------- ALL PLANS:")
        print(self.data)
        print("<--------- ALL PLANS FOR ROOMS:")
        print(self.data_rooms)
        print("<--------- ALL PLANS FOR TEACHERS:")
        print(self.data_teachers)

    def show_subject(subject):
        print("Subject:: " + str(subject.dayOfWeek) + " " + str(subject.whenStart) + " " + str(subject.whenFinnish))
