from django import forms
from accounts.models import *
from django.core.exceptions import ValidationError
from datetime import date
import re

class DateInput(forms.DateInput):
    input_type = 'date'

class MedicineForm(forms.ModelForm):

    class Meta:
        model = Medicines
        # fields = '__all__'
        exclude = ['expire']
        widgets = {
            'medicine':forms.TextInput(attrs={'class':'form-control'}),
            'stock':forms.NumberInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(MedicineForm, self).clean()
        medicine = self.cleaned_data.get('medicine')
        stock = self.cleaned_data.get('stock')

        for instance in Medicines.objects.all():
            if instance.medicine == medicine:
                self._errors['medicine'] = self.error_class(['Medicine already exists, Please update it if required'])

        if medicine.isdigit():
            self._errors['medicine'] = self.error_class(['Please enter a valid medicine name'])

        if re.findall('[()[\]\{\}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', medicine):
            self._errors['medicine'] = self.error_class(['Please enter a valid medicine name'])

        if stock < 0:
            self._errors['stock'] = self.error_class(['Invalid stock entered'])

        return self.cleaned_data


class SicknessForm(forms.ModelForm):

    class Meta:
        model = sickness_details
        exclude = ['status','animal','medicine']

        widgets = {
            'sdate':DateInput(attrs={'class':'form-control'}),
            'disease':forms.TextInput(attrs={'class':'form-control'}),
            'consumption':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(SicknessForm, self).clean()
        sdate = self.cleaned_data.get('sdate')
        disease = self.cleaned_data.get('disease')
        consumption = self.cleaned_data.get('consumption')
        
        if sdate.__gt__(date.today()):
            self._errors['sdate'] = self.error_class(['Not permitted to enter future date'])

        if disease.isdigit():
            self._errors['disease'] = self.error_class(['Enter a valid disease'])

        if not re.findall('[a-z]',disease) and not re.findall('[A-Z]',disease):
            self._errors['disease'] = self.error_class(['Please enter a valid disease'])

        if consumption.isdigit():
            self._errors['consumption'] = self.error_class(['Enter valid consumption details'])

        return self.cleaned_data


class DeathForm(forms.ModelForm):

    class Meta:
        model = Animals
        fields = ['death_date','death_cause','incineration']
        widgets = {
            'death_date':DateInput(attrs={'class':'form-control'}),
            'death_cause':forms.TextInput(attrs={'class':'form-control'}),
            'incineration':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(DeathForm, self).clean()
        ddate = self.cleaned_data.get('death_date')
        cause = self.cleaned_data.get('death_cause')
        incineration = self.cleaned_data.get('incineration')

        if ddate.__gt__(date.today()):
            self._errors['death_date'] = self.error_class(['Not permitted to enter future date'])

        if cause.isdigit():
            self._errors['death_cause'] = self.error_class(['Enter a valid cause of death'])

        if incineration.isdigit():
            self._errors['incineration'] = self.error_class(['Enter a valid inceneration details'])

        return self.cleaned_data
        