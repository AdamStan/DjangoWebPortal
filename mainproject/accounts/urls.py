from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login', views.show_login, name='logout'),
    path('logout', views.show_logout, name='login')
]
