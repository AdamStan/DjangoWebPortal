from datetime import time
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .views import test_user_is_admin, forbidden
from accounts.models import User
from .models import *
from django.http import HttpResponse


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_intro_edit_models(request):
    models_list = [
        "Building",
        "Faculty",
        "Field Of Study",
        "",
    ]

    return render(request, 'admin/edit_models.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_building(request):
    return render(request, 'admin/edit_models/tab_building.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_faculty(request):
    return render(request, 'admin/edit_models/tab_faculty.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_fieldofstudy(request):
    return render(request, 'admin/edit_models/tab_fieldofstudy.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_plan(request):
    return render(request, 'admin/edit_models/tab_plan.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_room(request):
    return render(request, 'admin/edit_models/tab_room.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_scheduledsubject(request):
    return render(request, 'admin/edit_models/tab_scheduledsubject.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_student(request):
    return render(request, 'admin/edit_models/tab_student.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_teacher(request):
    return render(request, 'admin/edit_models/tab_teacher.html')


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_user(request):
    return render(request, 'admin/edit_models/tab_user.html')
