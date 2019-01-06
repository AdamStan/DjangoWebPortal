from django.db import transaction
from numpy import array, nditer, zeros
from random import randint, choice
from datetime import time
from copy import deepcopy
from .algorithm import check_room_is_not_taken, check_teacher_can_teach, check_subject_to_subject_time
from .models import Room, Teacher, ScheduledSubject, Plan

class ImprovementManagerQuerySets:

    def __init__(self, plans, sch_subjects, teachers, rooms):
        self.scheduled_subjects = sch_subjects
        self.plans = plans
        self.day_of_week = [1, 2, 3, 4, 5, ]  # I've deleted 6 and 7 because we don't have saturday

    @transaction.atomic
    def generation(self, min_hour=8, max_hour=19):
        sid = transaction.savepoint()
        try:
            # 1. losujemy plan
            plan_to_change = choice(self.plans)
            print("Plan to change = " + str(plan_to_change))
            # 2. losujemy dzien do poki dzien nie jest pusty
            day = choice(self.day_of_week)
            while True:
                subjects_in_day = self.scheduled_subjects.filter(dayOfWeek=day, plan=plan_to_change)
                print("Przedmioty w dniu:" + str(subjects_in_day.count()))
                if subjects_in_day.count() == 0:
                    day = choice(self.day_of_week)
                else:
                    break
            # 3. z tego dnia wybieramy przedmiot
            subject_to_change = choice(subjects_in_day)
            ImprovementManagerQuerySets.show_subject(subject_to_change)
            # 4. liczymy wartosc planu
            value_before = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))
            value_after = 9999
            print("Value before: " + str(value_before))
            # 4.0.1 zapisujemy stare dane
            old = {
                "start_hour": subject_to_change.whenStart,
                "finish_hour": subject_to_change.whenFinnish,
                "day": subject_to_change.dayOfWeek,
            }
            # 4.1 jesli jest to lab
            if subject_to_change.type == "LAB":
                print("LAB, it is LAB")
                # 4.1.1 losujemy nowe wartosci
                subject_to_change.whenStart = time(randint(min_hour, max_hour),0,0)
                fin = subject_to_change.whenStart.hour + subject_to_change.how_long
                subject_to_change.whenFinnish = time(fin,0,0)
                subject_to_change.dayOfWeek = choice(self.day_of_week)
                # 4.1.2 check new value
                subject_to_change.save()
                ImprovementManagerQuerySets.show_subject(subject_to_change)

                value_after = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))
                print("New value:" + str(value_after))

                case1 = check_room_is_not_taken(subject_to_change, subject_to_change.room)
                case2 = check_teacher_can_teach(subject_to_change, subject_to_change.teacher)
                case3 = check_subject_to_subject_time(subject_to_change, self.scheduled_subjects.filter(plan=plan_to_change))
                if case1 and case2 and case3 and value_before > value_after:
                    print("Improving can be performed...")
                    transaction.savepoint_commit(sid)
                else:
                    print("Improving do not improve plans")
                    transaction.savepoint_rollback(sid)
            # 4.2 jesli jest to lec
            elif subject_to_change.type == "LEC":
                print("LEC, it is LEC")
                # 4.1.1 losujemy nowe wartosci
                new_whenStart = time(randint(min_hour, max_hour), 0, 0)
                fin = subject_to_change.whenStart.hour + subject_to_change.how_long
                new_whenFinnish = time(fin, 0, 0)
                new_dayOfWeek = choice(self.day_of_week)
                # 4.1.2 check new value
                # subject_to_change.save()
                # ImprovementManagerQuerySets.show_subject(subject_to_change)

                others_lectures = ScheduledSubject.objects.filter(subject=subject_to_change.subject)
                for sub in others_lectures:
                    ImprovementManagerQuerySets.show_subject(sub)
                #value_after = self.value_for_plan(subjects_in_plan=self.scheduled_subjects.filter(plan=plan_to_change))
                #print("New value:" + str(value_after))


                #case1 = check_room_is_not_taken(subject_to_change, subject_to_change.room)
                #case2 = check_teacher_can_teach(subject_to_change, subject_to_change.teacher)
                #case3 = check_subject_to_subject_time(subject_to_change,
                #                                      self.scheduled_subjects.filter(plan=plan_to_change))
                #if case1 and case2 and case3 and value_before > value_after:
                #    print("Improving can be performed...")
                #    transaction.savepoint_commit(sid)
                #else:
                #    print("Improving do not improve plans")

                transaction.savepoint_rollback(sid)
            # 3.1.3 losujemy te wartosci
            # 3.2 jesli jest to lec
            # transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            print(str(e))
            raise e

    def value_for_plan(self, subjects_in_plan):
        # wzor: liczba dni niepustych + (poczotek + koniec - czas trwania przedmiotow) <- dla kazdego dnia
        value = 5

        for day in self.day_of_week:
            subjects_how_long, first_hour, last_hour = 0, 24, 0
            list_of_subjects_in_one_day = subjects_in_plan.filter(dayOfWeek=day)
            for subject in list_of_subjects_in_one_day:
                if subject.whenStart.hour < first_hour:
                    first_hour = subject.whenStart.hour
                if subject.whenFinnish.hour > last_hour:
                    last_hour = subject.whenFinnish.hour
                subjects_how_long += subject.how_long

            if not list_of_subjects_in_one_day:  # checks that list is empty
                value -= 1
            else:
                value += last_hour - first_hour - subjects_how_long

        return value

    def show_subject(subject):
        print("[Subject:: " + str(subject.subject.name) + str(subject.dayOfWeek) + " " + str(subject.whenStart) + " " + str(subject.whenFinnish) + "]")


def make_improvement(how_many=1):
    scheduled_subjects = ScheduledSubject.objects.all()
    rooms = Room.objects.all().order_by("id")
    teachers = Teacher.objects.all().order_by("user_id")
    plans = Plan.objects.all().order_by("id")

    instance = ImprovementManagerQuerySets(plans=plans, sch_subjects=scheduled_subjects, teachers=teachers, rooms=rooms)
    for i in range(0,1):
        instance.generation()


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
                self.data[row][i-1] = list(scheduled_subjects.filter(dayOfWeek=i))
            row = row + 1

        row = 0
        for r in rooms:
            rooms_list.append(r)
            scheduled_subjects = subjects.filter(room=r)
            for i in range(1, self.day_of_week.size + 1):  # 1 2 3 4 5 6 7
                self.data_rooms[row][i - 1] = list(scheduled_subjects.filter(dayOfWeek=i))
            row = row + 1

        row = 0
        for t in teachers:
            teachers_list.append(t)
            scheduled_subjects = subjects.filter(teacher=t)
            for i in range(1, self.day_of_week.size + 1):  # 1 2 3 4 5 6 7
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
        which_day = choice(self.day_of_week) - 1 # because curva

        if not buff[which_day]:
            print("Empty day was chosen")
            return
        try:
            which_subject_index = randint(0, len(buff[which_day]) - 1)
        except ValueError:
            which_subject_index = 0

        subject_before = buff[which_day][which_subject_index]
        # workaround xD
        if subject_before.type == "LEC":
            print("I will try make improvement on lecture in future version, I swear")
        else:
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
            what_return = what_return and \
                          self.check_subject_to_teacher(subject=subject_after, which_day=subject_after.dayOfWeek - 1)
            what_return = what_return and \
                          self.check_subject_to_rooms(subject=subject_after, which_day=subject_after.dayOfWeek - 1)

            if not what_return:
                print("SOME CASE HAVE NOT PASSED")
                return

            # counts value for old plan
            value_before = self.value_for_plan(plan_position=which_plan_will_be_mutated)

            # set new subject to plan
            new_buff = self.changed_piece_of_plan(subject_after, subject_before, which_plan_will_be_mutated)
            for list_subjects in new_buff:
                ImprovementManager.show_subject_list(list_of_subject=list_subjects)
            # count value for new plan
            value_after = self.value_for_plan(plan=new_buff)

            if value_after < value_before:
                self.data[which_plan_will_be_mutated] = new_buff
                self.change_teachers_and_rooms_plan(subject_after=subject_after, subject_before=subject_before)
                print("Great job")
            else:
                self.data[which_plan_will_be_mutated] = buff
                print("Value after is the same or bigger")

    def value_for_plan(self, plan_position = -1, plan = array([])):
        # wzor: liczba dni niepustych + (poczotek + koniec - czas trwania przedmiotow) <- dla kazdego dnia
        if plan_position >= 0:
            buff_new = self.data[plan_position]
        elif plan.any():
            buff_new = plan
        else:
            raise Exception("GIVE PLAN POSITION OR PLAN TO ESTIMATE")
        print("VALUE FOR THIS PLAN:")
        value = 5
        for list_of_subjects in buff_new:
            ImprovementManager.show_subject_list(list_of_subjects)
            subjects_how_long, first_hour, last_hour = 0, 24, 0
            for subject in list_of_subjects:
                if subject.whenStart.hour < first_hour:
                    first_hour = subject.whenStart.hour
                if subject.whenFinnish.hour > last_hour:
                    last_hour = subject.whenFinnish.hour
                subjects_how_long += subject.how_long
            if not list_of_subjects: # checks that list is empty
                value -= 1
            else:
                value += last_hour - first_hour - subjects_how_long
        return value

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
        teacher_day = teachers_week[which_day]

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
        room_day = room_week[which_day]

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

    def changed_piece_of_plan(self, subject_after, subject_before, which_plan_will_be_mutated):
        new_plan = self.data[which_plan_will_be_mutated].copy()

        # removes old subject from plan
        for i in range(0, len(new_plan[subject_before.dayOfWeek - 1])):
            subject = new_plan[subject_before.dayOfWeek - 1][i]
            if subject.id == subject_before.id:
                new_plan[subject_before.dayOfWeek - 1].pop(i)
                break
        # sets new subject to plan
        new_plan[subject_after.dayOfWeek - 1].append(subject_after)

        return new_plan

    def change_teachers_and_rooms_plan(self, subject_after, subject_before):
        room_index = self.room_in_array(subject_before.room)

        # removes subject...
        for i in range(0, len(self.data_rooms[room_index][subject_before.dayOfWeek - 1])):
            subject = self.data_rooms[room_index][subject_before.dayOfWeek - 1][i]
            if subject.id == subject_after.id:
                self.data_rooms[room_index][subject_before.dayOfWeek - 1].pop(i)
                break

        # add subject
        self.data_rooms[room_index][subject_after.dayOfWeek - 1].append(subject_after)

        teacher_index = self.teacher_in_array(subject_before.teacher)
        # remove subject
        for i in range(0, len(self.data_teachers[teacher_index][subject_before.dayOfWeek - 1])):
            subject = self.data_teachers[teacher_index][subject_before.dayOfWeek - 1][i]
            if subject.id == subject_after.id:
                self.data_teachers[teacher_index][subject_before.dayOfWeek - 1].pop(i)
                break

        # add subject
        self.data_teachers[teacher_index][subject_after.dayOfWeek - 1].append(subject_after)

    def make_improvement(self, number_of_generation):
        for i in range(0, number_of_generation):
            self.generation()

        self.pass_to_database()

    def pass_to_database(self):
        for plans in self.data:
            for subject_list in plans:
                for subject in subject_list:
                    subject.save()

    def show_data(self):
        print(self.plans_ids)
        print("<--------- ALL PLANS:")
        print(self.data)
        print("<--------- ALL PLANS FOR ROOMS:")
        print(self.data_rooms)
        print("<--------- ALL PLANS FOR TEACHERS:")
        print(self.data_teachers)

    def show_subject(subject):
        print("[Subject:: " + str(subject.dayOfWeek) + " " + str(subject.whenStart) + " " + str(subject.whenFinnish) + "]")

    def show_subject_list(list_of_subject):
        show_list = ""
        for subject in list_of_subject:
            show_list += "[Subject:: " + str(subject.dayOfWeek) + " " + \
                         str(subject.whenStart) + " " + str(subject.whenFinnish) + "]"
        print(show_list)