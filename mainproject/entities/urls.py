from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'entities'

urlpatterns = [
    path('timetables/student', views.show_student_plans, name='timetables_student'),
    path('timetables/teacher', views.show_teachers_plans, name='timetables_teacher'),
    path('timetables/room', views.show_rooms_plans, name='timetables_room'),
    path('timetables/', views.show_timetables, name='timetables'),
    path('edittimetables', views.show_edit_timetable, name='edittimetables'),
    path('studentplans/', views.show_choose_plan, name='studentplans'),
    path('studentplan/', views.show_user_plan, name="studentplan"),
    path('teacherplan/', views.show_user_plan, name='teacherplan'),
    path('generate/', views.show_generate_page, name='generate')
]
