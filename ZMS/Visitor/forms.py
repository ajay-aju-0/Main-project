from django import forms
from accounts.models import *
from datetime import date,timedelta

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

    def clean(self):
        super(TicketForm, self).clean()
        rdate = self.cleaned_data.get('reporting_date')
        prior_date = date.today() + timedelta(days=3)

        time_obj = ZooTimings.objects.filter(holiday = True)

        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # print(rdate.weekday())
        if rdate.__lt__(date.today()):
            self._errors['reporting_date'] = self.error_class(['Preffered date already ended'])

        for i in time_obj:
            # print(i.day, weekday_names[rdate.weekday()])
            if i.day == weekday_names[rdate.weekday()]:
                self._errors['reporting_date'] = self.error_class(['Preffered date is holiday'])

        if  rdate > prior_date:
            self._errors['reporting_date'] = self.error_class(['You are only allowed to book ticket prior to 3 days'])

        return self.cleaned_data


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaints
        fields = ['complaint']
        widgets = {
            'complaint':forms.Textarea(attrs={'class':'form-control'}),
        }

    def clean(self):
        super(ComplaintForm, self).clean()
        complaint = self.cleaned_data.get('complaint')

        if complaint.isdigit():
            self._errors['complaint'] = self.error_class(['Complaint only contains digit.Please provide a valid complaint'])
               
        return self.cleaned_data


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Applications
        fields = ['qualification','cv']
        widgets = {
            'qualification':forms.TextInput(attrs={'class':'form-control'}),
            'cv':forms.FileInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(ApplicationForm, self).clean()
        qualification = self.cleaned_data.get('qualification')

        if qualification.isdigit():
            self._errors['qualification'] = self.error_class(['Please provide a valid qualification details'])

        return self.cleaned_data
