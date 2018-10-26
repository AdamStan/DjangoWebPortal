from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import datetime
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, active=True, is_student=False, is_teacher=False, is_scheduler=False, name=None, surname=None):
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have password")
        user_instance = self.__module__(username)
        user_instance.set_password(password)
        user_instance.is_active = active
        user_instance.student = is_student
        user_instance.teacher = is_teacher
        user_instance.scheduler = is_scheduler
        user_instance.name = name
        user_instance.surname = surname
        user_instance.save()
        return user_instance

    def create_student(self, username, password=None, active=True, name=None, surname=None):
        user_instance = self.create_user(
            username= username,
            password= password,
            active = active,
            is_student = True,
            name = name,
            surname = surname
        )
        return user_instance

    def create_teacher(self, username, password=None, active=True, name=None, surname=None):
        user_instance = self.create_user(
            username=username,
            password=password,
            active=active,
            is_teacher=True,
            name=name,
            surname=surname
        )
        return user_instance

    def create_scheduler(self, username, password=None, active=True, name=None, surname=None):
        user_instance = self.create_user(
            username=username,
            password=password,
            active=active,
            is_scheduler=True,
            name=name,
            surname=surname
        )
        return user_instance

class User(AbstractBaseUser):
    username = models.CharField(max_length=64, unique=True, default='USER_WITH_NONAME')
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=32, default=None)
    surname = models.CharField(max_length=64, default=None)
    whenCreated = models.DateField(default=datetime.date.today)
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