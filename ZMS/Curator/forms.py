from django import forms
from django.forms import fields,widgets
from accounts.models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class EnclosureForm(forms.ModelForm):

    class Meta:
        model = Enclosures
        fields = ['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'})
        }

class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animals
        exclude = ['death_date','death_cause','incineration','date_joined','akind','status','caretaker']

        location = forms.ModelChoiceField(
            queryset = Enclosures.objects.all(),
            to_field_name = 'location',
            required = True,
        )

        widgets = {
            'given_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'height':forms.NumberInput(attrs={'class':'form-control'}),
            'weight':forms.NumberInput(attrs={'class':'form-control'}),
            'birth_date':DateInput(attrs={'class':'form-control'}),
            'area_id':forms.TextInput(attrs={'class':'form-control'}),
            'health_status':forms.Select(attrs={'class':'form-control'}),
            'diatery_req':forms.Textarea(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'image1':forms.FileInput(attrs={'class':'form-control'}),
            'image2':forms.FileInput(attrs={'class':'form-control'}),
            'image3':forms.FileInput(attrs={'class':'form-control'}),
        }

class AnimalKindForm(forms.ModelForm):

    class Meta:
        model = AnimalKind
        exclude = ['class_id']
        widgets = {
            'general_name':forms.TextInput(attrs={'class':'form-control'}),
            'species':forms.TextInput(attrs={'class':'form-control'}),
            'avg_lifespan':forms.TextInput(attrs={'class':'form-control'}),
            'habitat':forms.TextInput(attrs={'class':'form-control'}),
            'origin':forms.TextInput(attrs={'class':'form-control'}),
            'Aorder':forms.TextInput(attrs={'class':'form-control'}),
            'characteristics':forms.Textarea(attrs={'class':'form-control'}),   
        }

class TaxonomyForm(forms.ModelForm):

    class Meta:
        model = Taxonomy
        fields = '__all__'
        widgets = {
            'Aclass':forms.Select(attrs={'class':'form-control'}),
        }

class UpdateAnimalForm(forms.ModelForm):

    class Meta:
        model = Animals
        exclude = ['death_date','death_cause','incineration','date_joined','akind','status','caretaker']

        location = forms.ModelChoiceField(
            queryset = Enclosures.objects.all(),
            to_field_name = 'location',
            required = True,
        )

        widgets = {
            'given_name':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'height':forms.NumberInput(attrs={'class':'form-control'}),
            'weight':forms.NumberInput(attrs={'class':'form-control'}),
            'birth_date':DateInput(attrs={'class':'form-control'}),
            'area_id':forms.TextInput(attrs={'class':'form-control'}),
            'health_status':forms.Select(attrs={'class':'form-control'}),
            'diatery_req':forms.Textarea(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
        }

class AnimalOfTheWeekForm(forms.ModelForm):

    class Meta:
        model = Animal_of_the_week
        exclude = ['animal_week_date']

        animal = forms.ModelChoiceField(
            queryset = Animals.objects.all(),
            to_field_name = 'animal',
            required = True,
        )

        widgets = {
            'animal':forms.Select(attrs={'class':'form-control'}),
            'performance':forms.FileInput(attrs={'class':'form-control'})
        }

class TransferDetailsForm(forms.ModelForm):

    class Meta:
        model = TransferDetails
        fields = '__all__'

        animal = forms.ModelChoiceField(
            queryset = Animals.objects.all(),
            to_field_name = 'animal',
            required = True,
        )

        widgets = {
            'animal':forms.Select(attrs={'class':'form-control'}),
            'transfer_from':forms.TextInput(attrs={'class':'form-control'}),
            'transfer_to':forms.TextInput(attrs={'class':'form-control'}),
            'transfer_date':DateInput(attrs={'class':'form-control'}),
            'reason':forms.TextInput(attrs={'class':'form-control'}),
        }

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'item':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'pdate':DateInput(attrs={'class':'form-control'}),
        }

class StaffRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','gender','dob','country','state','city','street','pincode','house_name','email','username','password','id_card')
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
        }
        help_texts = {'username':None}
