import threading
import multiprocessing as mp
from datetime import time
from .algorithm import OnePlanGenerator

class CreatePlan:
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