from django import forms
from .models import *


class CreateBuilding(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'


class CreateFaculty(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'


