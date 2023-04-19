from django import forms
from django.forms import fields,widgets
from accounts.models import *
import re
from datetime import date

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class EnclosureForm(forms.ModelForm):

    class Meta:
        model = Enclosures
        fields = ['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(EnclosureForm, self).clean()
        name = self.cleaned_data.get('name')

        if any(char.isdigit() for char in name) == True:
            self._errors['name'] = self.error_class(['Enclosure name will not contain numbers'])

        if re.findall('[()[\]\{\}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', name):
            self._errors['name'] = self.error_class(['Enclosure name will not contain any symbols'])

        for instance in Enclosures.objects.all():
            if instance.name.lower() == str(name).lower():
                self._errors['name'] = self.error_class(['Enclosure already exists'])

        return self.cleaned_data        


class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animals
        exclude = ['death_date','death_cause','incineration','date_joined','akind','status','caretaker','reason']

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

    def clean(self):
        super(AnimalForm, self).clean()
        name = self.cleaned_data.get('given_name')
        diet = self.cleaned_data.get('diatery_req')
        bdate = self.cleaned_data.get('birth_date')

        for instance in Animals.objects.all():
            if instance.given_name.lower() == str(name).lower():
                self._errors['given_name'] = self.error_class(['An animal with this name already exists'])

        if name.isdigit():
            self._errors['given_name'] = self.error_class(['Aniaml name will not contain numbers only'])

        if re.findall('[()[\]\{\}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', name):
            self._errors['given_name'] = self.error_class(['Animal name will not contain any symbols'])

        if diet.isdigit():
            self._errors['diatery_req'] = self.error_class(['Please provide valid diet for this animal'])

        if bdate > date.today():
            self._errors['birth_date'] = self.error_class(['Future date can\'t be set as birth date'])
    
        return self.cleaned_data


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

    def clean(self):
        super(AnimalKindForm, self).clean()
        name = self.cleaned_data.get('general_name')
        species = self.cleaned_data.get('species')
        habitat = self.cleaned_data.get('habitat')
        origin = self.cleaned_data.get('origin')
        order = self.cleaned_data.get('Aorder')
        characteristics = self.cleaned_data.get('characteristics')

        if any(char.isdigit() for char in name) == True:
            self._errors['name'] = self.error_class(['Invalid animal name'])

        if any(char.isdigit() for char in species) == True:
            self._errors['species'] = self.error_class(['Invalid species name specified'])

        if any(char.isdigit() for char in habitat) == True:
            self._errors['habitat'] = self.error_class(['Habitat will not contain numbers'])

        if any(char.isdigit() for char in origin) == True:
            self._errors['origin'] = self.error_class(['Invalid origin specified'])

        if any(char.isdigit() for char in order) == True:
            self._errors['Aorder'] = self.error_class(['Invalid animal order specified'])

        if characteristics.isdigit():
            self._errors['characteristics'] = self.error_class(['Please provide valid characteristics of this animal'])

        return self.cleaned_data


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
        exclude = ['death_date','death_cause','incineration','date_joined','akind','status','caretaker','reason']

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

    def clean(self):
        super(UpdateAnimalForm, self).clean()
        name = self.cleaned_data.get('given_name')
        diet = self.cleaned_data.get('diatery_req')
        bdate = self.cleaned_data.get('birth_date')
        
        if diet.isdigit():
            self._errors['diatery_req'] = self.error_class(['Please provide valid diet for this animal'])

        if bdate > date.today():
            self._errors['birth_date'] = self.error_class(['Future date can\'t be set as birth date'])
    
    
        return self.cleaned_data


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
            'order':forms.TextInput(attrs={'class':'form-control'}),
            'animal':forms.Select(attrs={'class':'form-control'}),
            'transfer_from':forms.TextInput(attrs={'class':'form-control'}),
            'transfer_to':forms.TextInput(attrs={'class':'form-control'}),
            'transfer_date':DateInput(attrs={'class':'form-control'}),
            'transfer_time':TimeInput(attrs={'class':'form-control'}),
            'transport_type':forms.TextInput(attrs={'class':'form-control'}),
            'transport_company':forms.TextInput(attrs={'class':'form-control'}),
            'transporter_name':forms.TextInput(attrs={'class':'form-control'}),
            'transporter_contact':forms.NumberInput(attrs={'class':'form-control'}),
            'reason':forms.TextInput(attrs={'class':'form-control'}),
            'expense':forms.NumberInput(attrs={'class':'form-control'})
        }

    def clean(self):
        super(TransferDetailsForm, self).clean()
        reason = self.cleaned_data.get('reason')
        expense = self.cleaned_data.get('expense')
        tdate = self.cleaned_data.get('transfer_date')
        ttype = self.cleaned_data.get('transport_type')
        tcompany = self.cleaned_data.get('transport_company')
        tname = self.cleaned_data.get('transporter_name')
        contact = self.cleaned_data.get('transporter_contact')

        if reason.isdigit():
            self._errors['reason'] = self.error_class(['enter a valid reason'])

        if expense < 0:
            self._errors['expense'] = self.error_class(['Enter a valid expense'])

        if tdate > date.today():
            self._errors['transfer_date'] = self.error_class(['Future transfers are not allowed to enter'])

        if ttype.isdigit():
            self._errors['transport_type'] = self.error_class(['enter a valid type of transportation'])

        if tcompany.isdigit():
            self._errors['transport_company'] = self.error_class(['enter a valid company name'])

        if tname.isdigit():
            self._errors['transporter_name'] = self.error_class(['enter a valid name'])

        if len(str(contact)) < 10:
            self._errors['transporter_contact'] = self.error_class(['contact number will be minimum of 10 digit'])

        return self.cleaned_data


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

    def clean(self):
        super(PurchaseForm, self).clean()
        item = self.cleaned_data.get('item')
        quantity = self.cleaned_data.get('quantity')
        price = self.cleaned_data.get('price')
        pdate = self.cleaned_data.get('pdate')

        if item.isdigit():
            self._errors['item'] = self.error_class(['Enter a valid item name'])

        if quantity < 0:
            self._errors['quantity'] = self.error_class(['Enter a valid quantity'])

        if price < 0:
            self._errors['price'] = self.error_class(['Enter a valid price'])
    
        if pdate > date.today():
            self._errors['pdate'] = self.error_class(['Future purchases are not allowed to enter'])
    
        return self.cleaned_data


class StaffRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','gender','dob','country','state','city','street','pincode','house_name','email','username','password','id_card','profile')
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
            'profile':forms.FileInput(attrs={'class':'form-control'}),

        }
        help_texts = {'username':None}

    def clean(self):
        super(StaffRegistrationForm, self).clean()
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
        