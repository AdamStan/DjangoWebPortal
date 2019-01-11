from datetime import time
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.shortcuts import render
from .views import test_user_is_admin, forbidden
from accounts.models import User, UserManager
from accounts.forms import MyAccountUpdate
from .models import *
from django.http import HttpResponse


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_intro_edit_models(request):
    url_list = {
        "Building":"model_building",
        "Faculty":"model_faculty",
        "Field Of Study":"model_fieldofstudy",
        "Plan":"model_plan",
        "Room":"model_room",
        "Scheduled Subject":"model_scheduledsubject",
        "Subject":"model_subject",
    }

    return render(request, 'admin/edit_models.html', {"urls": url_list})


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
    users = User.objects.filter(admin=True)
    s_message = ""
    fail_message = ""
    if request.method == "POST":
        action = request.POST.get('action')
        print(action)
        user_id = request.POST.get('user_id')
        if action == "Edit":
            user_to_edit = User.objects.filter(id=user_id)
            print("User: ")
            return render(request, 'admin/edit_models/forms/edit_form_admin.html', {"user_to_edit": user_to_edit[0]})
        elif action == "Change_password":
            print("CHANGE " + user_id)
            user_to_edit = User.objects.filter(id=user_id)
            return render(request, 'admin/edit_models/forms/change_password.html', {"user_to_edit": user_to_edit[0]})
        elif action == "Delete":
            User.objects.filter(id=user_id).delete()
            users = User.objects.filter(admin=True)
            s_message = "User was deleted successfully "
        elif action == "Update":
            username = request.POST.get("username")
            name = request.POST.get("name")
            second_name = request.POST.get("second_name")
            surname = request.POST.get("surname")
            user_to_edit = User.objects.filter(id=user_id)
            user_to_edit = user_to_edit[0]
            user_to_edit.username = username
            user_to_edit.name = name
            user_to_edit.second_name = second_name
            user_to_edit.surname = surname
            print(user_to_edit)
            user_to_edit.save()
            s_message = "User was updated successfully"
            users = User.objects.filter(admin=True)
        elif action == "Add_admin":
            return render(request, 'admin/edit_models/forms/add_user.html')
        elif action == "Do_change_password":
            user_to_edit = User.objects.filter(id=user_id)
            user_to_edit = user_to_edit[0]
            new_password = request.POST.get("new_password")
            confirm_new_password = request.POST.get("confirm_new_password")
            if new_password == confirm_new_password:
                user_to_edit.set_password(new_password)
                user_to_edit.save()
                s_message = "Password was changed successfully"
                users = User.objects.filter(admin=True)
            else:
                fail_message = "Passwords are not the same"
        elif action == "Do_add_user":
            username = request.POST.get("username")
            name = request.POST.get("name")
            second_name = request.POST.get("second_name")
            surname = request.POST.get("surname")
            password = request.POST.get("password")
            manager = UserManager()
            manager.create_superuser(username=username, password=password, active=True, name=name, surname=surname, snmae=second_name)
            users = User.objects.filter(admin=True)
    return render(request, 'admin/edit_models/tab_user.html', {"admins": users, "s_message": s_message, "fail_message": fail_message})
