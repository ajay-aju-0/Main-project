from django import forms
from accounts.models import *
from datetime import date

class DateInput(forms.DateInput):
    input_type = 'date'

class ConsumptionForm(forms.ModelForm):

    class Meta:
        model = ConsumptionDetails
        fields = ['dose','date']
        widgets = {
            'dose':forms.NumberInput(attrs={'class':'form-control'}),
            'date':DateInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(ConsumptionForm, self).clean()
        dose = self.cleaned_data.get('dose')
        cdate = self.cleaned_data.get('date')

        if dose < 0:
            self._errors['dose'] = self.error_class(['Please provide valid no. of dose'])

        if dose == 0:
            self._errors['dose'] = self.error_class(['Please provide no. of dose given'])

        if cdate.__gt__(date.today()):
            self._errors['date'] = self.error_class(['Future date is not permissible'])

        return self.cleaned_data