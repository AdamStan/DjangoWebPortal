from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from entities.models import *
# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=64)
    #types of users:
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    scheduler = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =  ['name', 'surname']

    def __str__(self):
        return self.name + ', ' + self.surname

    @property
    def is_student(self):
        return self.student

    @property
    def is_teacher(self):
        return self.teacher

    @property
    def is_scheduler(self):
        return self.scheduler

class Student(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True, related_name='student_to_user')
    #fieldOfStudy
    yearOfStudy = models.DateTimeField()
    #currentSubjects

class Teacher(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True, related_name='professor_to_user')
    #faculty
    #subjects

class Scheduler(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True, related_name='scheduler_to_user')