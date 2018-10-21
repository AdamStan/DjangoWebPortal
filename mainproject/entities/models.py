from django.db import models

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=64)

class Subject(models.Model):
    name = models.CharField(max_length=128)
    faculty = Faculty()

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64)

class ScheduledSubject(models.Model):
    hours = models.DateTimeField()

class Plan(models.Model):
    title = models.CharField(max_length=32)
    #schedule
