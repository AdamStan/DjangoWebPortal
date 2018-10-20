from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=128)

class Schedule(models.Model):
    name = models.CharField(max_length=32)

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=64)

class Faculty(models.Model):
    name = models.CharField(max_length=64)

class ScheduledSubject(models.Model):
    hours = models.DateTimeField()
