from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_scheduler = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=64)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=64)

class Scheduler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)