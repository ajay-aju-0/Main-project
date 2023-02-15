from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    gen_choice = (('m','male'),('f','female'))
    con_choice = (('Afghanistan', 'Afghanistan'),('Albania', 'Albania'),('Algeria', 'Algeria'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Antigua and Barbuda', 'Antigua and Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),('Botswana', 'Botswana'),('Brazil', 'Brazil'),
        ('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Cabo Verde', 'Cabo Verde'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Congo', 'Congo'),('Costa Rica', 'Costa Rica'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Cyprus', 'Cyprus'),('Czech Republic', 'Czech Republic'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini', 'Eswatini'),('Ethiopia', 'Ethiopia'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Greece', 'Greece'),('Grenada', 'Grenada'),('Guatemala', 'Guatemala'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Honduras', 'Honduras'),('Hungary', 'Hungary'),('Iceland','Iceland'),("India", "India"),("Indonesia", "Indonesia"),("Iran", "Iran"),
        ("Iraq", "Iraq"),("Ireland", "Ireland"),('Israel', 'Israel'),('Italy', 'Italy'),('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('North Korea', 'North Korea'),('South Korea', 'South Korea'),('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),
        ('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar', 'Myanmar'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('North Macedonia', 'North Macedonia'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Qatar', 'Qatar'),('Romania', 'Romania'),('Russia', 'Russia'),('Rwanda', 'Rwanda'),('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),('Saint Lucia', 'Saint Lucia'),('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),('Samoa', 'Samoa'),('San Marino', 'San Marino'), ('Sao Tome and Principe','Sao Tome and Principe'), ('Saudi Arabia','Saudi Arabia'), ('Senegal','Senegal'), ('Serbia','Serbia'), ('Seychelles','Seychelles'), ('Sierra Leone','Sierra Leone'),('Singapore','Singapore'), ('Slovakia','Slovakia'),
        ('Slovenia','Slovenia'), ('Solomon Islands','Solomon Islands'), ('Somalia','Somalia'), ('South Africa','South Africa'), ('South Sudan','South Sudan'), ('Spain','Spain'), ('Sri Lanka','Sri Lanka'), ('Sudan','Sudan'), ('Suriname','Suriname'), ('Sweden','Sweden'), ('Switzerland','Switzerland'), ('Syria','Syria'), ('Taiwan','Taiwan'), ('Tajikistan','Tajikistan'), ('Tanzania','Tanzania'), ('Thailand','Thailand'), ('Timor-Leste','Timor-Leste'), ('Togo','Togo'), ('Tonga','Tonga'), ('Trinidad and Tobago','Trinidad and Tobago'), ('Tunisia','Tunisia'), ('Turkey','Turkey'), ('Turkmenistan','Turkmenistan'), ('Tuvalu','Tuvalu'), ('Uganda','Uganda'), ('Ukraine','Ukraine'),
        ('United Arab Emirates','United Arab Emirates'), ('United Kingdom','United Kingdom'), ('United States','United States'), ('Uruguay','Uruguay'), ('Uzbekistan','Uzbekistan'), ('Vanuatu','Vanuatu'), ('Vatican City','Vatican City'), ('Venezuela','Venezuela'), ('Vietnam','Vietnam'), ('Yemen','Yemen'), ('Zambia','Zambia'), ('Zimbabwe','Zimbabwe')
    )
    gender = models.CharField(max_length=1,choices=gen_choice)
    dob = models.DateField()
    country = models.CharField(max_length=32,choices=con_choice)
    state =models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    pincode = models.IntegerField()
    house_name = models.CharField(max_length=50)
    phone = models.BigIntegerField(default=0)
    usertype = models.CharField(max_length=15)
    id_card = models.FileField(upload_to="id",max_length=300)

class Staffs(models.Model):
    desig = models.CharField(max_length=20,verbose_name="designation")
    salary = models.BigIntegerField()
    bonus = models.IntegerField()
    user = models.ForeignKey(to=Users,on_delete=models.CASCADE)

class TicketRate(models.Model):
    type = models.CharField(max_length=20,verbose_name="ticket type")
    rate = models.IntegerField()

class Ticket(models.Model):
    tdate = models.DateField(auto_now_add=True)
    adult_no = models.IntegerField(default=0)
    child_no = models.IntegerField(default=0)
    student_no = models.IntegerField(default=0)
    total = models.IntegerField()
    reporting_date = models.DateTimeField(null=False)
    paid = models.BooleanField()
    uid = models.ForeignKey(to=Users,on_delete=models.CASCADE)
    Guide = models.ForeignKey(to=Staffs,on_delete=models.CASCADE,default="not assigned")

class Feedback(models.Model):
    feedback = models.CharField(max_length=250)
    reply = models.CharField(max_length=200,null=True)
    uid = models.ForeignKey(to=Users,on_delete=models.CASCADE)

class Complaints(models.Model):
    complaint = models.CharField(max_length=250)
    reply = models.CharField(max_length=200,null=True)
    uid = models.ForeignKey(to=Users,on_delete=models.CASCADE)

class Locations(models.Model):
    name = models.CharField(max_length=20,verbose_name="location name")
    archieved = models.BooleanField(default=False)

class Taxonomy(models.Model):
    Aorder = models.CharField(max_length=30,primary_key=True)
    Aclass = models.CharField(max_length=30)

class AnimalKind(models.Model):
    general_name = models.CharField(max_length=30)
    species = models.CharField(max_length=30)
    avg_lifespan = models.CharField(max_length=25)
    habitat = models.CharField(max_length=250,verbose_name="natural habitat")
    origin = models.CharField(max_length=20)
    Aorder = models.ForeignKey(to=Taxonomy,on_delete=models.CASCADE)
    characteristics = models.CharField(max_length=200)

class Animals(models.Model):
    choice = (('m','male'),('f','female'))
    given_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1,choices=choice)
    height = models.FloatField()
    weight = models.FloatField()
    birth_date = models.DateField()
    death_date = models.DateField(null=True,default="")
    death_cause = models.CharField(max_length=100,null=True)
    incineration = models.CharField(max_length=100,null=True)
    location = models.ForeignKey(to=Locations,on_delete=models.CASCADE)
    area_id = models.CharField(max_length=10)
    health_status = models.CharField(max_length=10)
    status = models.BooleanField()
    diatery_req = models.CharField(max_length=100,verbose_name='diatery requirement')
    caretaker = models.ForeignKey(to=Staffs,on_delete=models.CASCADE)
    akind = models.ForeignKey(to=AnimalKind,on_delete=models.CASCADE)

class TransferDetails(models.Model):
    animal = models.ForeignKey(to=Animals,on_delete=models.CASCADE)
    transfer_from = models.CharField(max_length=25)
    transfer_to = models.CharField(max_length=25)
    transfer_date = models.DateField()
    reason = models.CharField(max_length=150,verbose_name="transfer_reason")

class Animal_of_the_week(models.Model):
    animal = models.ForeignKey(to=Animals,on_delete=models.CASCADE)
    performance = models.FileField(upload_to="performances",max_length=300)
    an_week_date = models.DateField()

class Medicines(models.Model):
    medicine = models.CharField(max_length=30)
    stock = models.IntegerField()

class sickness_details(models.Model):
    animal = models.ForeignKey(to=Animals,on_delete=models.CASCADE)
    disease = models.CharField(max_length=50)
    medicine = models.ForeignKey(to=Medicines,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

class Purchase(models.Model):
    unit_choice = (('g','g'),('kg','kg'),('q','q'),('l','l'),('ml','ml'),('mm','mm'),('cm','cm'),('inch','inch'),('m','m'),('count','count'))
    item = models.CharField(max_length=25)
    quantity = models.FloatField()
    unit = models.CharField(max_length=5,choices=unit_choice)
    price = models.BigIntegerField()
    pdate = models.DateField()

class Events(models.Model):
    ename = models.CharField(max_length=30)
    estart = models.DateField()
    eend = models.DateField()
    eimage = models.FileField(upload_to='events',max_length=300)
    estatus = models.CharField(max_length=10)

class Participants(models.Model):
    event = models.ForeignKey(to=Events,on_delete=models.CASCADE)
    animal = models.ForeignKey(to=Animals,on_delete=models.CASCADE)

class JobVacancy(models.Model):
    type_choice = (("temporary","temporary"),("permenant","permenant"))
    status_choice = (("available","available"),("closed","closed"))
    vposition = models.CharField(max_length=25,verbose_name="vacancy position")
    qualification = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    vtype = models.CharField(max_length=10,choices=type_choice)
    vstart = models.DateField(verbose_name="start date")
    vend = models.DateField(verbose_name="end date")
    vstatus = models.CharField(max_length=10,choices=status_choice)

class Applications(models.Model):
    fullname = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.BigIntegerField()
    cv = models.FileField(upload_to="cv",max_length=300)
    vacancy = models.ForeignKey(to=JobVacancy,on_delete=models.CASCADE)
    status = models.CharField(max_length=10)