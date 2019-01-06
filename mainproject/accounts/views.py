from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import MyAccountUpdate
from .models import User
# Create your views here.


def show_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html',{'form':form})


def show_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    return redirect('homepage')


@login_required
def show_my_profile(request):
    user = request.user
    if request.POST:
        old_form = [
            request.POST.get('username'),
            request.POST.get('password'),
            request.POST.get('name'),
            request.POST.get('second_name'),
            request.POST.get('surname'),
        ]
        print(old_form)
        user = User.objects.get(username=request.user.username)
        user.username = old_form[0]
        if old_form[1] != None and old_form[1][7:13] != "sha256" and old_form[1] != "":
            user.set_password(old_form[1])
            print(old_form[1][7:13])
        user.name  = old_form[2]
        user.second_name = old_form[3]
        user.surname = old_form[4]
        user.save()

    form = MyAccountUpdate({
        'username': user.username,
        'password': user.password,
        'name': user.name,
        'second_name': user.second_name,
        'surname': user.surname
    })
    return render(request, 'myprofile.html', {'current_user': user, 'form': form} )
