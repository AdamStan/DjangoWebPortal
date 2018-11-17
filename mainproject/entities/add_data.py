from .models import *
from acconts.models import User

def add_data():
    faculty1 = Faculty(name="EEIA")
    faculty1.save()
    teacher1 = Teacher()