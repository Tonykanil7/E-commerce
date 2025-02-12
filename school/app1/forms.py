from django import forms
from app1.models import School
from django.forms import PasswordInput
from django.contrib.auth.models import User

class Schoolform(forms.ModelForm):
    location_choices = [('ekm', 'EKM'), ('tvm', 'TVM'),('ktm','KTM')]
    location = forms.ChoiceField(choices=location_choices, widget=forms.Select, required=True)
    class Meta:
        model=School
        fields=['name','location','principal']

class Regform(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    class Meta:
        model=User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']