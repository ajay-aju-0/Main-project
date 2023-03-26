from django import forms
from accounts.models import *
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'

class MedicineForm(forms.ModelForm):

    class Meta:
        model = Medicines
        fields = '__all__'
        widgets = {
            'medicine':forms.TextInput(attrs={'class':'form-control'}),
            'stock':forms.NumberInput(attrs={'class':'form-control'})
        }

class SicknessForm(forms.ModelForm):

    class Meta:
        model = sickness_details
        exclude = ['status']

        animal = forms.ModelChoiceField(
            queryset = Animals.objects.all(),
            to_field_name = 'animal',
            required = True,
        )

        medicine = forms.ModelChoiceField(
            queryset = Medicines.objects.all(),
            to_field_name = 'medicine',
            required = True
        )

        widgets = {
            'animal':forms.Select(attrs={'class':'form-control'}),
            'sdate':DateInput(attrs={'class':'form-control'}),
            'disease':forms.TextInput(attrs={'class':'form-control'}),
            'medicine':forms.Select(attrs={'class':'form-control'})

        }

class DeathForm(forms.ModelForm):

    class Meta:
        model = Animals
        fields = ['death_date','death_cause','incineration']
        widgets = {
            'death_date':DateInput(attrs={'class':'form-control'}),
            'death_cause':forms.TextInput(attrs={'class':'form-control'}),
            'incineration':forms.TextInput(attrs={'class':'form-control'})
        }

class ReasonForm(forms.ModelForm):

    class Meta:
        model = Animals
        fields = ['reason']
        widgets = {
            'reason':forms.Textarea(attrs={'class':'form-control'})
        }