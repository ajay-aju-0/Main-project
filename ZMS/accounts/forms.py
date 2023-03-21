from django import forms
from django.forms import fields,widgets
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','gender','dob','country','state','city','street','pincode','house_name','email','username','password','usertype','id_card','profile')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'country':forms.Select(attrs={'class':'form-control'}),
            'state':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'street':forms.TextInput(attrs={'class':'form-control'}),
            'pincode':forms.TextInput(attrs={'class':'form-control'}),
            'house_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'dob':DateInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'id_card':forms.FileInput(attrs={'class':'form-control'}),
            'usertype':forms.TextInput(attrs={'class':'form-control','type':'hidden'}),
            'profile':forms.FileInput(attrs={'class':'form-control'})
        }
        help_texts = {'username':None}


class VacancyForm(forms.ModelForm):

    class Meta:
        model = JobVacancy
        exclude = ('issue_date','vstatus')
        widgets = {
            'vposition':forms.TextInput(attrs={'class':'form-control'}),
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'vtype':forms.Select(attrs={'class':'form-control'}),
            'vstart':DateInput(attrs={'class':'form-control'}),
            'vend':DateInput(attrs={'class':'form-control'}),
        }
