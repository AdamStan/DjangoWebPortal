from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

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
    return render(request, 'login.html', {'form': form})

def show_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    return redirect('homepage')