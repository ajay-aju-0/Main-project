from django import forms
from accounts.models import *
from django.core.exceptions import ValidationError

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


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staffs
        exclude = ['user']
        widgets = {
            'desig' : forms.TextInput(attrs={"class":"form-control"}),
            'salary' : forms.NumberInput(attrs={"class":"form-control"}),
            'bonus' : forms.NumberInput(attrs={"class":"form-control"}),
        }


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
        print(catagory)

        def isNum(data):
            try:
                int(data)
                return True
            except ValueError:
                return False

        for instance in TicketRate.objects.all():
            if instance.type == catagory:
                # print(instance.type,catagory)
                self._errors['type'] = self.error_class(['catagory already exists'])
        
        if isNum(catagory):
                self._errors['type'] = self.error_class(['catagory cannot be integer'])
            


        return self.cleaned_data


class UpdateTicketRateForm(forms.ModelForm):

    class Meta:
        model = TicketRate
        fields = '__all__'
        widgets = {
            'type' : forms.TextInput(attrs={"class":"form-control"}),
            'rate' : forms.NumberInput(attrs={"class":"form-control"}),
        }

class ZooTimeForm(forms.ModelForm):

    class Meta:
        model = ZooTimings
        fields = '__all__'
        widgets = {
            'day':forms.TextInput(attrs={'class':'form-control'}),
            'open_time':forms.TextInput(attrs={'class':'form-control'}),
            'close_time':forms.TextInput(attrs={'class':'form-control'})
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

class UpdateEventForm(forms.ModelForm):

    class Meta:
        model = Events
        exclude = ['estatus']
        widgets = {
            'ename':forms.TextInput(attrs={'class':'form-control'}),
            'estart':DateInput(attrs={'class':'form-control'}),
            'eend':DateInput(attrs={'class':'form-control'}),
        }

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
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'sdate':DateInput(attrs={'class':'form-control'}),
            'edate':DateInput(attrs={'class':'form-control'}),
            'notes':forms.Textarea(attrs={'class':'form-control'})
        }

class SponseredAnimalForm(forms.ModelForm):

    class Meta:
        model = SponseredAnimals
        fields = ['animal']

        animal = forms.ModelChoiceField(
            queryset = Animals.objects.all(),
            to_field_name = 'animal',
            required = True,
        )
        widgets={
            'animal':forms.Select(attrs={'class':'form-control'})
        }

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

class DateInput(forms.DateInput):
    input_type = 'date'


class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','gender','dob','country','state','city','street','pincode','house_name','email','username','id_card','profile')
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