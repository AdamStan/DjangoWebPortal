from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'entities'

urlpatterns = [
    path('timetables/', views.show_timetables, name='timetables'),
    path('studentplans/', views.show_student_plans, name='studentplans'),
    path('teacherplan/', views.show_teacher_plan, name='teacherplan')
]
