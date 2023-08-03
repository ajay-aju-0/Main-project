from django import forms
from .models import *
from datetime import date
import re


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
            'pincode':forms.NumberInput(attrs={'class':'form-control'}),
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

    def clean(self):
        super(RegistrationForm, self).clean()
        firstName = self.cleaned_data.get('first_name')
        lastName = self.cleaned_data.get('last_name')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        phone = self.cleaned_data.get('phone')
        houseName = self.cleaned_data.get('house_name')
        userName = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if firstName == '':
            self._errors['first_name'] = self.error_class(['First name cannot be null'])
        
        if any(char.isdigit() for char in firstName) or any(char.isdigit() for char in lastName):
            self._errors['first_name'] = self.error_class(['name will not contain a number, enter a valid name'])
            self._errors['last_name'] = self.error_class(['name will not contain a number, enter a valid name'])
        
        if any(char.isdigit() for char in state):
            self._errors['state'] = self.error_class(['state will not contain a number, enter a valid state'])
        
        if any(char.isdigit() for char in city):
            self._errors['city'] = self.error_class(['city will not contain a number, enter a valid city'])
        
        if phone < 0:
            self._errors['phone'] = self.error_class(['Please provide a valid phone no.'])
        
        if len(str(phone)) < 10:
            self._errors['phone'] = self.error_class(['Phone no. will contain atleast 10 numbers'])
        
        if houseName.isdigit():
            self._errors['house_name'] = self.error_class(['House name will not contain only numbers'])
        
        if any(uname.isdigit() for uname in userName) == False:
            self._errors['username'] = self.error_class(['username must contain atleast 1 number'])
        
        if len(userName) < 5 and len(userName) >15:
            self._errors['username'] = self.error_class(['username must contain minimum 5 and maximum 15 characters'])
        
        if userName[0].isalpha() == False:
            self._errors['username'] = self.error_class(['First character must be an alphabhet'])
        
        if userName[-1] == '_':
            self._errors['username'] = self.error_class(['username cannot end with an underscore'])
        
        if len(password) < 8:
            self._errors['password'] = self.error_class(['Password must contain atleast 8 characters'])
        
        if password.isdigit():
            self._errors['password'] = self.error_class(['password is entirely numeric'])
        
        if any(pwd.isdigit() for pwd in password) == False:
            self._errors['password'] = self.error_class(['password must contain atleast 1 digit'])
        
        if not re.findall('[A-Z]',password):
            self._errors['password'] = self.error_class(['password must contain atleast 1 uppercase letter'])

        if not re.findall('[a-z]',password):
            self._errors['password'] = self.error_class(['password must contain atleast 1 lowercase letter'])

        if not re.findall('[()[\]\{\}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            self._errors['password'] = self.error_class(['password must contain at least 1 symbol:()[]\{\}|\`~!@#$%^&*_-+=;:\'",<>./?'])

        return self.cleaned_data
        

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
            'order':forms.TextInput(attrs={'class':'form-control'}),
            'vstart_time':forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'vend_time':forms.TimeInput(attrs={'class':'form-control','type':'time'}),
        }

    def clean(self):
        super(VacancyForm, self).clean()
        position = self.cleaned_data.get('vposition')
        qualification = self.cleaned_data.get('qualification')
        description = self.cleaned_data.get('description')
        start = self.cleaned_data.get('vstart')
        end = self.cleaned_data.get('vend')

        if any(char.isdigit() for char in position):
            self._errors['vposition'] = self.error_class(['position will not contain a number, enter a valid position'])
        
        if qualification.isdigit():
            self._errors['qualification'] = self.error_class(['Enter valid qualification details'])
        
        if description.isdigit():
            self._errors['description'] = self.error_class(['Given description contains only numbers'])
        
        if start.__gt__(end):
            self._errors['vend'] = self.error_class(['End date should be greater than start date'])
        
        if start.__lt__(date.today()):
            self._errors['vstart'] = self.error_class(['Given date is already ended'])
        
        if end.__lt__(date.today()):
            self._errors['vend'] = self.error_class(['Given date is already ended'])

        return self.cleaned_data
        