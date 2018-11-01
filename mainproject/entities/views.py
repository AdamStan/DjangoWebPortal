from django.shortcuts import render

def show_timetables(request):
    return render(request, 'timetables.html');