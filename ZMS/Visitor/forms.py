from django import forms
from accounts.models import *
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['feedback']
        widgets = {
            'feedback':forms.Textarea(attrs={'class':'form-control'})
        }


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        exclude = ['tdate','total','uid','Guide','total_person','payment_status']
        widgets = {
            'reporting_date':DateInput(attrs={'class':'form-control'}),
            'reporting_time':forms.Select(attrs={'class':'form-control'}),
        }

class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaints
        fields = ['complaint']
        widgets = {
            'complaint':forms.Textarea(attrs={'class':'form-control'}),
        }

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Applications
        fields = ['qualification','cv']
        widgets = {
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'cv':forms.FileInput(attrs={'class':'form-control'})
        }
        