from django.db import models
from accounts.models import User # it works, really

var_on_delete = models.SET_NULL = True

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default=None)

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty, on_delete=var_on_delete, default=None)
    degree = models.IntegerField(default=None)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='professor_to_user')
    faculty = models.ForeignKey(Faculty, on_delete=var_on_delete)

class Subject(models.Model):
    name = models.CharField(max_length=128)
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete, default=None)
    yearOfStudy = models.IntegerField(default=None)
    teachers = models.ManyToManyField(Teacher)

class Building(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    numberOfBuilding = models.CharField(max_length=8)
    postalCode = models.CharField(max_length=8)

class Room(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    building = models.ForeignKey(Building, on_delete=var_on_delete)

class Plan(models.Model):
    title = models.CharField(max_length=32)
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete, default=None)

class ScheduledSubject(models.Model):
    subject = models.OneToOneField(Subject, on_delete=var_on_delete, default=None)
    whenStart = models.TimeField(default=None)
    whenFinnish = models.TimeField(default=None)
    dayOfWeek = models.CharField(max_length=32, default=None)
    plan = models.ForeignKey(Plan, on_delete=var_on_delete, default=None)
    room = models.ForeignKey(Room, on_delete=var_on_delete, default=None)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_to_user')
    fieldOfStudy = models.ForeignKey(FieldOfStudy, on_delete=var_on_delete)
    yearOfStudy = models.IntegerField(default=None)
    degree = models.IntegerField(default=None)
    plan = models.ForeignKey(Plan, on_delete=var_on_delete, default=None)