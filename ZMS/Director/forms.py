from django import forms
from accounts.models import *
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'


class CuratorForm(forms.ModelForm):

    class Meta:
        model = Staffs
        exclude = ['user','desig']
        widgets = {
            'salary' : forms.NumberInput(attrs={"class":"form-control"}),
            'bonus' : forms.NumberInput(attrs={"class":"form-control"}),
        }

    def clean(self):
        super(CuratorForm, self).clean()
        salary = self.cleaned_data.get('salary')

        if salary == 0:
            self._errors['salary'] = self.error_class(['Please provide salary of the curator'])
        
        if salary < 0:
            self._errors['salary'] = self.error_class(['Please provide a valid salary'])
        
        return self.cleaned_data


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staffs
        exclude = ['user']
        widgets = {
            'desig' : forms.TextInput(attrs={"class":"form-control"}),
            'salary' : forms.NumberInput(attrs={"class":"form-control"}),
            'bonus' : forms.NumberInput(attrs={"class":"form-control"}),
        }

    def clean(self):
        super(StaffForm, self).clean()
        designation = self.cleaned_data.get('desig')
        salary = self.cleaned_data.get('salary')

        if designation == '':
            self._errors['desig'] = self.error_class(['Please provide designation of the staff'])
        
        if any(char.isdigit() for char in designation) == True:
            self._errors['desig'] = self.error_class(['Designation will not contain numbers'])
        
        if salary == 0:
            self._errors['salary'] = self.error_class(['Please provide salary of the curator'])
        
        if salary < 0:
            self._errors['salary'] = self.error_class(['Please provide a valid salary'])
        
        return self.cleaned_data


class TicketRateForm(forms.ModelForm):

    class Meta:
        model = TicketRate
        fields = '__all__'
        widgets = {
            'type' : forms.TextInput(attrs={"class":"form-control"}),
            'rate' : forms.NumberInput(attrs={"class":"form-control"}),
        }

    def clean(self):
        super(TicketRateForm,self).clean()
        catagory = self.cleaned_data.get('type')
        trate = self.cleaned_data.get('rate')
        # print(catagory)
        
        for instance in TicketRate.objects.all():
            if instance.type == catagory:
                # print(instance.type,catagory)
                self._errors['type'] = self.error_class(['catagory already exists'])
        
        if catagory.isdigit():
                self._errors['type'] = self.error_class(['catagory cannot be integer'])

        if trate < 0:
            self._errors['rate'] = self.error_class(['Please provide valid rate'])
            
        return self.cleaned_data


class ZooTimeForm(forms.ModelForm):

    class Meta:
        model = ZooTimings
        exclude = ['holiday']
        widgets = {
            'day':forms.TextInput(attrs={'class':'form-control'}),
            'open_time':forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'close_time':forms.TimeInput(attrs={'class':'form-control','type':'time'})
        }


class EventForm(forms.ModelForm):

    class Meta:
        model = Events
        exclude = ['estatus']
        widgets = {
            'ename':forms.TextInput(attrs={'class':'form-control'}),
            'estart':DateInput(attrs={'class':'form-control'}),
            'eend':DateInput(attrs={'class':'form-control'}),
            'eimage':forms.FileInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(EventForm, self).clean()
        event = self.cleaned_data.get('ename')
        start = self.cleaned_data.get('estart')
        end = self.cleaned_data.get('eend')

        if event.isdigit():
            self._errors['ename'] = self.error_class(['Event name will not contain only numbers'])
        
        if start.__gt__(end):
            self._errors['eend'] = self.error_class(['End date should be greater than start date'])
        
        if start.__lt__(date.today()):
            self._errors['estart'] = self.error_class(['Given date is already ended'])
        
        if end.__lt__(date.today()):
            self._errors['eend'] = self.error_class(['Given date is already ended'])

        return self.cleaned_data


class UpdateEventForm(forms.ModelForm):

    class Meta:
        model = Events
        exclude = ['estatus']
        widgets = {
            'ename':forms.TextInput(attrs={'class':'form-control'}),
            'estart':DateInput(attrs={'class':'form-control'}),
            'eend':DateInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        super(UpdateEventForm, self).clean()
        event = self.cleaned_data.get('ename')
        start = self.cleaned_data.get('estart')
        end = self.cleaned_data.get('eend')

        if event.isdigit():
            self._errors['ename'] = self.error_class(['Event name will not contain only numbers'])
        
        if start.__gt__(end):
            self._errors['eend'] = self.error_class(['End date should be greater than start date'])
        
        if start.__lt__(date.today()):
            self._errors['estart'] = self.error_class(['Given date is already ended'])
        
        if end.__lt__(date.today()):
            self._errors['eend'] = self.error_class(['Given date is already ended'])

        return self.cleaned_data


class SponserForm(forms.ModelForm):

    class Meta:
        model = SponserDetails
        exclude = ['joined_date']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'stype':forms.Select(attrs={'class':'form-control'}),
            'notes':forms.Textarea(attrs={'class':'form-control'})
        }

    def clean(self):
        super(SponserForm, self).clean()
        name = self.cleaned_data.get('name')
        address = self.cleaned_data.get('address')
        phone = self.cleaned_data.get('phone')
        notes = self.cleaned_data.get('notes')

        if any(char.isdigit() for char in name):
            self._errors['name'] = self.error_class(['Name will not contain any numbers'])
        
        if address.isdigit():
            self._errors['address'] = self.error_class(['Address contains only numbers'])

        if phone < 0:
            self._errors['phone'] = self.error_class(['Please provide a valid phone no.'])
        
        if len(str(phone)) < 10:
            self._errors['phone'] = self.error_class(['Phone no. will contain atleast 10 numbers'])

        if notes.isdigit():
            self._errors['notes'] = self.error_class(['notes contains only numbers'])

        return self.cleaned_data

class UpdateSponserForm(forms.ModelForm):

    class Meta:
        model = SponserDetails
        exclude = ['joined_date']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','readonly':True,'disabled':True}),
            'address':forms.Textarea(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'stype':forms.Select(attrs={'class':'form-control'}),
            'notes':forms.Textarea(attrs={'class':'form-control'})
        }

    def clean(self):
        super(UpdateSponserForm, self).clean()
        address = self.cleaned_data.get('address')
        phone = self.cleaned_data.get('phone')
        notes = self.cleaned_data.get('notes')

        if address.isdigit():
            self._errors['address'] = self.error_class(['Address contains only numbers'])

        if phone < 0:
            self._errors['phone'] = self.error_class(['Please provide a valid phone no.'])
        
        if len(str(phone)) < 10:
            self._errors['phone'] = self.error_class(['Phone no. will contain atleast 10 numbers'])

        if notes.isdigit():
            self._errors['notes'] = self.error_class(['notes contains only numbers'])

        return self.cleaned_data



class SponseredAnimalForm(forms.ModelForm):

    class Meta:
        model = SponseredAnimals
        exclude = ['sponser']

        animal = forms.ModelChoiceField(
            queryset = Animals.objects.all(),
            to_field_name = 'animal',
            required = True,
        )

        widgets={
            'animal':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'sdate':DateInput(attrs={'class':'form-control'}),
            'edate':DateInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        super(SponseredAnimalForm, self).clean()
        amount = self.cleaned_data.get('amount')
        start = self.cleaned_data.get('sdate')
        end = self.cleaned_data.get('edate')

        if amount == 0:
            self._errors['amount'] = self.error_class(['Enter the sponsership amount'])
        
        if amount < 0:
            self._errors['amount'] = self.error_class(['Enter a valid amount'])

        if start.__gt__(end):
            self._errors['edate'] = self.error_class(['End date should be greater than start date'])
        
        if start.__lt__(date.today()):
            self._errors['sdate'] = self.error_class(['Given date is already ended'])
        
        if end.__lt__(date.today()):
            self._errors['edate'] = self.error_class(['Given date is already ended'])

        return self.cleaned_data                 
        

class ZooDetailsForm(forms.ModelForm):

    class Meta:
        model = ZooDetails
        exclude = ['current_animal_occupancy','enclosure_types']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'total_animal_capacity':forms.NumberInput(attrs={'class':'form-control'}),
            'visitor_capacity':forms.NumberInput(attrs={'class':'form-control'}),
            'total_area':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(ZooDetailsForm, self).clean()
        name = self.cleaned_data.get('name')
        location = self.cleaned_data.get('location')
        capacity = self.cleaned_data.get('total_animal_capacity')
        vcapacity = self.cleaned_data.get('visitor_capacity')

        if any(char.isdigit() for char in name):
            self._errors['name'] = self.error_class(['Name will not contain any numbers'])
        
        if any(char.isdigit() for char in location):
            self._errors['location'] = self.error_class(['Location cannot contain any numbers'])

        if capacity == 0:
            self._errors['total_animal_capacity'] = self.error_class(['Enter the maximum animal capacity'])
        
        if capacity < 0:
            self._errors['total_animal_capacity'] = self.error_class(['Enter a valid capacity'])

        if vcapacity == 0:
            self._errors['visitor_capacity'] = self.error_class(['Enter the visitor capacity'])
        
        if vcapacity < 0:
            self._errors['visitor_capacity'] = self.error_class(['Enter a valid capacity'])
        
        return self.cleaned_data
         

class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','gender','dob','country','state','city','street','pincode','house_name','email','username','id_card')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
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
        }
        help_texts = {'username':None}

    def clean(self):
        super(UpdateProfileForm, self).clean()
        firstName = self.cleaned_data.get('first_name')
        lastName = self.cleaned_data.get('last_name')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        phone = self.cleaned_data.get('phone')
        houseName = self.cleaned_data.get('house_name')
        userName = self.cleaned_data.get('username')
        
        if firstName == '':
            self._errors['first_name'] = self.error_class(['First name cannot be null'])
        
        if any(char.isdigit() for char in firstName) or any(char.isdigit() for char in lastName):
            self._errors['first_name'] = self.error_class(['name will not contain a number, enter a valid name'])
            self._errors['last_name'] = self.error_class(['name will not contain a number, enter a valid name'])
        
        if any(char.isdigit() for char in state):
            self._errors['state'] = self.error_class(['state will not contain a number, enter a valid state'])
        
        if any(char.isdigit() for char in city):
            self._errors['city'] = self.error_class(['city will not contain a number, enter a valid city'])
        
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
        
        return self.cleaned_data


class ProfileImageForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['profile']