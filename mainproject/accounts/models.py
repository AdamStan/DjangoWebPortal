from django.contrib.auth.models import AbstractBaseUser
from django.db import models
# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=64)
    whenCreated = models.DateField(auto_now_add=True)
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