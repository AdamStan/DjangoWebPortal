from django.db import models
import json
from accounts.models import User # it works, really

var_on_delete = models.SET_NULL = True

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default=None, null=True)

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty, on_delete=var_on_delete, default=None)
    BACHELOR = '1st'
    MASTER = '2nd'
    UNIFORM_MASTER_DEGREE = 'only-master'
    DEGREE_CHOICES = (
        (BACHELOR, 'bachelor'),
        (MASTER, 'master'),
        (UNIFORM_MASTER_DEGREE, 'only-master')
    )
    degree = models.CharField(max_length=12, choices=DEGREE_CHOICES, default=BACHELOR)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='professor_to_user')
    faculty = models.ForeignKey(Faculty, on_delete=var_on_delete)

class Subject(models.Model):
    name = models.CharField(max_length=128)
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete, default=None)
    semester = models.IntegerField(default=None)
    teachers = models.ManyToManyField(Teacher)

    def toJSON(self):
        return json.dumps(self.__dict__)

class Building(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    numberOfBuilding = models.CharField(max_length=8)
    postalCode = models.CharField(max_length=8)

class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    building = models.ForeignKey(Building, on_delete=var_on_delete, null=True)

class Plan(models.Model):
    title = models.CharField(max_length=32)
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete, default=None)

class ScheduledSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=var_on_delete, default=None, null=True)
    whenStart = models.TimeField(default=None)
    whenFinnish = models.TimeField(default=None)
    dayOfWeek = models.CharField(max_length=32, default=None)
    plan = models.ForeignKey(Plan, on_delete=var_on_delete, default=None)
    room = models.ForeignKey(Room, on_delete=var_on_delete, default=None)

    def toJSON(self):
        return json.dumps(self.__dict__)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_to_user')
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete)
    semester = models.IntegerField(default=1)
    degree = models.IntegerField(default=None)
    plan = models.ForeignKey(Plan, on_delete=var_on_delete, default=None, null=True)