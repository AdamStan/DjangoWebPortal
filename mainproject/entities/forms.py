from django import forms
from .models import Building


class CreateBuilding(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'


