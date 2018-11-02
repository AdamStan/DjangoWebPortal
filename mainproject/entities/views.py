from django.shortcuts import render

def create_table(start_hour = 8, end_hour = 20):
    value = start_hour
    r = end_hour - start_hour + 1
    values = []
    for i in range(r):
        values.append(value + i)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return {'values': values, 'days':days }

def show_timetables(request):
    parameters = create_table()
    return render(request, 'admin/timetables.html', parameters);

def show_student_plans(request):
    parameters = create_table()
    pass

def show_teacher_plan(request):
    parameters = create_table()
    pass