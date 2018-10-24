from django.db import models
from ..accounts.models import User
# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=64)

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64)
    faculty = models.ForeignKey(Faculty)
    degree = models.IntegerField()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='professor_to_user')
    faculty = models.ForeignKey(Faculty)

class Subject(models.Model):
    name = models.CharField(max_length=128)
    fieldOfStudy = models.ForeignKey(FieldOfStudy)
    yearOfStudy = models.IntegerField()
    teachers = models.ManyToManyField(Teacher)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_to_user')
    fieldOfStudy = models.ForeignKey(FieldOfStudy)
    yearOfStudy = models.IntegerField()
    degree = models.IntegerField()
    hoursInWeek = models.IntegerField()

class Building(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    numberOfBuilding = models.CharField(max_length=8)
    postalCode = models.CharField(max_length=8)

class Room(models.Model):
    id = models.CharField(primary_key=True)
    building = models.ForeignKey(Building)

class ScheduledSubject(models.Model):
    subject = models.OneToOneField(Subject)
    whenStart = models.TimeField()
    whenFinnish = models.TimeField()
    dayOfWeek = models.CharField()

class Plan(models.Model):
    title = models.CharField(max_length=32)
    subjects = models.ForeignKey(ScheduledSubject)
