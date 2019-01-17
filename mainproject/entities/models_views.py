from datetime import time
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from .views import test_user_is_admin, forbidden
from accounts.models import User, UserManager
from .models import *
from . import forms


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_intro_edit_models(request):
    url_list = {
        "Building":"model_building",
        "Faculty":"model_faculty",
        "Field Of Study":"model_field_of_study",
        "Plan":"model_plan",
        "Room":"model_room",
        "Scheduled Subject":"model_scheduledsubject",
        "Subject":"model_subject",
    }

    return render(request, 'admin/edit_models.html', {"urls": url_list})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_building(request):
    buildings = Building.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Building"
    columns = ['name','street','city','number','postal code']
    if request.method == "POST":
        action = request.POST.get("action")
        id = request.POST.get("object_id")
        if action == "Delete" and id:
            Building.objects.filter(id=id).delete()
            buildings = Building.objects.all()
            s_message = "Building was removed successfully"
        elif action == "Edit" and id:
            instance = Building.objects.filter(id=id)[0]
            form = forms.CreateBuilding(instance=instance)
            return render(request,'admin/edit_models/forms_model/add_model.html', {"object_id": id, "model_name": model_name,
                                                                                   "form_my": form, "act": "Update"})
        elif action == "Add":
            form = forms.CreateBuilding()
            return render(request, 'admin/edit_models/forms_model/add_model.html', {"model_name": model_name,
                                                                                    "form_my": form, "act": "Set"})
        elif action == "Set":
            form = forms.CreateBuilding(request.POST)
            if form.is_valid():
                form.save()
            buildings = Building.objects.all()
        elif action == "Update" and id:
            instance = get_object_or_404(Building, id=id)
            form = forms.CreateBuilding(request.POST)
            if form.is_valid():
                new_building = form.save(commit=False)
                new_building.id = instance.id
                new_building.save()
            buildings = Building.objects.all()
        else:
            fail_message = "You have to choose row"
    return render(request, 'admin/edit_models/tab_building.html',{"objects": buildings, "columns": columns,
                                                                  "s_message": s_message, "fail_message":fail_message})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_faculty(request):
    faculties = Faculty.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Faculty"
    columns = ['name', 'description']

    if request.method == "POST":
        action = request.POST.get('action')
        id = request.POST.get('object_id')
        if action == "Add":
            form = forms.CreateFaculty()
            return render(request, 'admin/edit_models/forms_model/add_model.html', {"model_name": model_name,
                                                                                    "form_my": form, "act": "Set"})
        elif action == "Edit" and id:
            instance = Faculty.objects.filter(id=id)[0]
            form = forms.CreateFaculty(instance=instance)
            return render(request, 'admin/edit_models/forms_model/add_model.html', {"object_id": id, "model_name": model_name,
                                                                             "form_my": form, "act": "Update"})
        elif action == "Delete" and id:
            faculty_to_delete = Faculty.objects.filter(id=id)
            fields = FieldOfStudy.objects.filter(faculty=faculty_to_delete[0])
            for field in fields:
                field.faculty = None
                field.save()
            teachers = Teacher.objects.filter(faculty=faculty_to_delete[0])
            for teacher in teachers:
                teacher.faculty = None
                teacher.save()
            faculty_to_delete[0].delete()

            faculties = Faculty.objects.all()
            s_message = "Faculty was deleted"
        elif action == "Set":
            form = forms.CreateFaculty(request.POST)
            if form.is_valid():
                form.save()
            faculties = Faculty.objects.all()
        elif action == "Update":
            instance = get_object_or_404(Faculty, id=id)
            form = forms.CreateFaculty(request.POST)
            if form.is_valid():
                new_faculty = form.save(commit=False)
                new_faculty.id = instance.id
                new_faculty.save()
            faculties = Faculty.objects.all()
        else:
            fail_message = "You have to choose field of study to " + action.lower()

    return render(request, 'admin/edit_models/tab_faculty.html', {"objects": faculties, "s_message": s_message,
                                                                  "fail_message": fail_message, "model_name": model_name, "columns": columns})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_fieldofstudy(request):
    fields_of_study = FieldOfStudy.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Field_of_study"
    columns = ['name', 'faculty name', 'degree', 'number of semesters', 'type']

    if request.method == "POST":
        action = request.POST.get('action')
        id = request.POST.get('object_id')
        if action == "Add":
            form = forms.CreateFieldOfStudy()
            return render(request, 'admin/edit_models/forms_model/add_model.html', {"model_name": model_name,
                                                                                    "form_my": form, "act": "Set"})
        elif action == "Edit" and id:
            instance = FieldOfStudy.objects.get(id=id)
            form = forms.CreateFieldOfStudy(instance=instance)
            return render(request, 'admin/edit_models/forms_model/add_model.html', {"object_id": id, "model_name": model_name,
                                                                                    "form_my": form, "act": "Update"})
        elif action == "Delete" and id:
            field_of_study = FieldOfStudy.objects.get(id=id)
            students = Student.objects.filter(fieldOfStudy=field_of_study)
            if students:
                fail_message = "You cannot drop this, there are students for this field"
            else:
                field_of_study.delete()
                s_message = "Chosen field was deleted"
                fields_of_study = FieldOfStudy.objects.all()
        elif action == "Set":
            form = forms.CreateFieldOfStudy(request.POST)
            if form.is_valid():
                form.save()
            s_message = "You've add new field of study"
        elif action == "Update":
            instance = get_object_or_404(FieldOfStudy, id=id)
            form = forms.CreateFieldOfStudy(request.POST)
            if form.is_valid():
                field_of_study = form.save(commit=False)
                field_of_study.id = instance.id
                field_of_study.save()
                s_message = "Changes were saved"
            fields_of_study = FieldOfStudy.objects.all()
        else:
            fail_message = "You have to choose field of study to " + action.lower()

    return render(request, 'admin/edit_models/tab_fieldofstudy.html', {"objects": fields_of_study, "s_message": s_message,
                                                                       "fail_message": fail_message, "model_name": model_name,
                                                                       "columns": columns})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_plan(request):
    plans = Plan.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Plan"
    columns = ['title', 'fieldOfStudy', 'semester']

    if request.method == "POST":
        action = request.POST.get('action')
        id = request.POST.get('object_id')
        if action == "Add":
            pass
        elif action == "Edit" and id:
            pass
        elif action == "Delete" and id:
            pass
        elif action == "Set":
            pass
        elif action == "Update":
            pass
        else:
            fail_message = "You have to choose field of study to " + action.lower()

    return render(request, 'admin/edit_models/tab_plan.html', {"objects": plans, "s_message": s_message,
                                                                "fail_message": fail_message, "model_name": model_name,
                                                                "columns": columns})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_room(request):
    rooms = Room.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Room"
    columns = ['id','building','room_type']

    if request.method == "POST":
        action = request.POST.get('action')
        id = request.POST.get('object_id')
        if action == "Add":
            pass
        elif action == "Edit" and id:
            pass
        elif action == "Delete" and id:
            pass
        elif action == "Set":
            pass
        elif action == "Update":
            pass
        else:
            fail_message = "You have to choose field of study to " + action.lower()

    return render(request, 'admin/edit_models/tab_room.html', {"objects": rooms, "s_message": s_message,
                                                                "fail_message": fail_message, "model_name": model_name,
                                                                "columns": columns})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_scheduledsubject(request):
    sch_subjects = ScheduledSubject.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Scheduledsubject"
    columns = ['subject name', 'type', 'plan', 'room', 'teacher']

    if request.method == "POST":
        action = request.POST.get('action')
        id = request.POST.get('object_id')

        if action == "Edit" and id:
            pass
        elif action == "Update":
            pass
        else:
            fail_message = "You have to choose field of study to " + action.lower()

    return render(request, 'admin/edit_models/tab_scheduledsubject.html', {"objects": sch_subjects, "s_message": s_message,
                                                                           "fail_message": fail_message, "model_name": model_name,
                                                                           "columns": columns})

def show_subject(request):
    subjects = Subject.objects.all()
    s_message = ""
    fail_message = ""
    model_name = "Subject"
    columns = ['name', 'fieldOfStudy', 'semester', 'lecture_hours', 'laboratory_hours', 'teachers',]

    if request.method == "POST":
        action = request.POST.get('action')
        id = request.POST.get('object_id')
        if action == "Add":
            pass
        elif action == "Edit" and id:
            pass
        elif action == "Delete" and id:
            pass
        elif action == "Set":
            pass
        elif action == "Update":
            pass
        else:
            fail_message = "You have to choose field of study to " + action.lower()

    return render(request, 'admin/edit_models/tab_subject.html', {"objects": subjects, "s_message": s_message,
                                                                  "fail_message": fail_message, "model_name": model_name,
                                                                  "columns": columns})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_student(request):
    students = Student.objects.all()
    s_message = ""
    fail_message = ""
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get('user_id')
        if action == "Edit" and user_id:
            student_to_edit = Student.objects.filter(user_id=user_id)
            fields_of_study = FieldOfStudy.objects.all().exclude(id=student_to_edit[0].fieldOfStudy.id)
            plans = Plan.objects.filter(fieldOfStudy=student_to_edit[0].fieldOfStudy, semester=student_to_edit[0].semester)
            return render(request, 'admin/edit_models/forms/edit_form_student.html',
                          {"student": student_to_edit[0], "fields_of_study": fields_of_study, "plans": plans})
        elif action == "Change_password" and user_id:
            student_to_edit = Student.objects.filter(user_id=user_id)
            return render(request, 'admin/edit_models/forms/change_password.html',
                          {"student_to_edit": student_to_edit[0], "model": "model_student"})
        elif action == "Delete" and user_id:
            Student.objects.filter(user_id=user_id).delete()
            User.objects.filter(id=user_id).delete()
            students = Student.objects.all()
            s_message = "User was deleted successfully "
        elif action == "Update" and user_id:
            #try:
            username = request.POST.get("username")
            name = request.POST.get("name")
            second_name = request.POST.get("second_name")
            surname = request.POST.get("surname")
            field_of_study = request.POST.get("field_of_study")
            semester = request.POST.get("semester")
            plan = request.POST.get("plan_id")
            student_to_edit = Student.objects.filter(user_id=user_id)
            student_to_edit = student_to_edit[0]
            student_to_edit.user.username = username
            student_to_edit.user.name = name
            student_to_edit.user.second_name = second_name
            student_to_edit.user.surname = surname
            student_to_edit.semester = semester
            if plan:
                student_to_edit.plan = Plan.objects.filter(id=plan)[0]
            if field_of_study:
                student_to_edit.fieldOfStudy = FieldOfStudy.objects.filter(id=field_of_study)[0]
            student_to_edit.user.save()
            student_to_edit.save()
            students = Student.objects.all()
            s_message = "Student was edited successfully"
            #except Exception:
            #    fail_message = "Something went wrong"
        elif action == "Add_student":
            fields = FieldOfStudy.objects.all()
            return render(request, 'admin/edit_models/forms/add_form_student.html', {"fields_of_study": fields})
        elif action == "Do_change_password":
            user_to_edit = User.objects.filter(id=user_id)
            user_to_edit = user_to_edit[0]
            new_password = request.POST.get("new_password")
            confirm_new_password = request.POST.get("confirm_new_password")
            if new_password == confirm_new_password:
                user_to_edit.set_password(new_password)
                user_to_edit.save()
                s_message = "Password was changed successfully"
                students = Student.objects.all()
            else:
                fail_message = "Passwords are not the same"
        elif action == "Do_add_user":
            try:
                username = request.POST.get("username")
                name = request.POST.get("name")
                second_name = request.POST.get("second_name")
                surname = request.POST.get("surname")
                password = request.POST.get("password")
                field_of_study = request.POST.get("field_of_study")
                semester = request.POST.get("semester")
                user = UserManager().create_student(username=username, password=password, active=True, name=name, sname=second_name, surname=surname)
                user.save()
                student_to_add = Student()
                student_to_add.user = user
                student_to_add.semester = semester
                if field_of_study:
                    student_to_add.fieldOfStudy = FieldOfStudy.objects.filter(id=field_of_study)[0]
                student_to_add.user.save()
                student_to_add.save()
                students = Student.objects.all()
                s_message = "Student was edited successful"
            except Exception:
                fail_message="Something went wrong"
        else:
            fail_message = "You should choose student before " + action.lower()
    return render(request, 'admin/edit_models/tab_student.html',{'students': students, "s_message": s_message, "fail_message": fail_message})


@user_passes_test(test_user_is_admin, login_url=forbidden)
def show_teacher(request):
    teachers = Teacher.objects.all()
    s_message = ""
    fail_message = ""
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get('user_id')
        if action == "Edit":
            teacher = Teacher.objects.filter(user_id=user_id)[0]
            faculties = Faculty.objects.exclude(id=teacher.faculty.id)
            return render(request, 'admin/edit_models/forms/edit_form_teacher.html', {"faculties": faculties, "teacher": teacher})
        elif action == "Change_password":
            teacher = Teacher.objects.filter(user_id=user_id)
            return render(request, 'admin/edit_models/forms/change_password.html', {"teacher": teacher[0], "model": "model_teacher"})
        elif action == "Delete":
            Teacher.objects.filter(user_id=user_id).delete()
            User.objects.filter(id=user_id).delete()
            teachers = Teacher.objects.all()
            s_message = "User was deleted successfully "
        elif action == "Update":
            username = request.POST.get("username")
            name = request.POST.get("name")
            second_name = request.POST.get("second_name")
            surname = request.POST.get("surname")
            faculty = request.POST.get('faculty')
            teacher = Teacher.objects.filter(user_id=user_id)[0]
            teacher.user.username = username
            teacher.user.name = name
            teacher.user.second_name = second_name
            teacher.user.surname = surname
            teacher.user.save()
            if faculty:
                teacher.faculty = Faculty.objects.filter(id=faculty)[0]
            teacher.save()
            s_message = "Editing teacher finished with success"
            teachers = Teacher.objects.all()
        elif action == "Add_teacher":
            faculties = Faculty.objects.all()
            return render(request, 'admin/edit_models/forms/add_form_teacher.html', {"faculties": faculties})
        elif action == "Do_change_password":
            user_to_edit = User.objects.filter(id=user_id)
            user_to_edit = user_to_edit[0]
            new_password = request.POST.get("new_password")
            confirm_new_password = request.POST.get("confirm_new_password")
            if new_password == confirm_new_password:
                user_to_edit.set_password(new_password)
                user_to_edit.save()
                s_message = "Password was changed successfully"
                teachers = Teacher.objects.all()
            else:
                fail_message = "Passwords are not the same"
        elif action == "Do_add_teacher":
            username = request.POST.get("username")
            name = request.POST.get("name")
            second_name = request.POST.get("second_name")
            surname = request.POST.get("surname")
            password = request.POST.get("password")
            faculty = request.POST.get('faculty')
            manager = UserManager()
            user = manager.create_teacher(username=username, password=password, active=True, name=name, surname=surname,
                                     sname=second_name)
            teacher = Teacher()
            teacher.user = user
            if faculty:
                teacher.faculty = Faculty.objects.filter(id=faculty)[0]
            teacher.save()
            s_message = "Adding new teacher finished with success"
            teachers = Teacher.objects.all()
        elif action == "Add_to_subject":
            pass
    return render(request, 'admin/edit_models/tab_teacher.html', {"teachers": teachers, "s_message": s_message, "fail_message": fail_message})


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
            return render(request, 'admin/edit_models/forms/edit_form_admin.html', {"user_to_edit": user_to_edit[0]})
        elif action == "Change_password":
            print("CHANGE " + user_id)
            user_to_edit = User.objects.filter(id=user_id)
            return render(request, 'admin/edit_models/forms/change_password.html', {"user_to_edit": user_to_edit[0], "model":"model_user"})
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
            return render(request, 'admin/edit_models/forms/add_form_user.html')
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
