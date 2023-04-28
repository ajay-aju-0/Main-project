from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from .forms import *
from Visitor.forms import ComplaintForm
from Director.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date


@login_required()
def loadDoctorHome(request):
    animal_obj = Animals.objects.filter(status = 1).count()
    medicine_in_stock = Medicines.objects.exclude(stock = 0).count()
    medicine_out_stock = Medicines.objects.filter(stock = 0).count()
    sick_animals = sickness_details.objects.filter(status = 'sick').values('sdate')
    cured_animals = sickness_details.objects.filter(status = 'cured').values('sdate')
    acceptedObj = Animals.objects.filter(reason = 'null').values('date_joined')
    rejectedObj = Animals.objects.exclude(reason = 'null').values('date_joined')
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()



    # print(medicine_in_stock, medicine_out_stock)

    sick = []
    cured = []
    accepted = []
    rejected = []

    for i in sick_animals:
        if i['sdate'].year == date.today().year and i['sdate'].month == date.today().month:
            sick.append(i)

    for i in cured_animals:
        if i['sdate'].year == date.today().year and i['sdate'].month == date.today().month:
            cured.append(i)

    for i in acceptedObj:
        if i['date_joined'].year == date.today().year and i['date_joined'].month == date.today().month:
            accepted.append(i)

    for i in rejectedObj:
        if i['date_joined'].year == date.today().year and i['date_joined'].month == date.today().month:
            rejected.append(i)

    context = {
        'animals':animal_obj,
        'med_stock':medicine_in_stock,
        'med_out':medicine_out_stock,
        'sick_animals':len(sick),
        'cured_animals':len(cured),
        'accepted':len(accepted),
        'rejected':len(rejected),
        'unverified_animals':request.session.get('unverified_animals_count')
    }

    
    return render(request,'doctorHome.html',context)


@login_required()
def animalVerification(request):
    animals = Animals.objects.all()
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    return render(request,'verify animals.html',{'animals':animals,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def verifyAnimal(request,id):
    animal = Animals.objects.get(pk=id)
    animal.status = 1
    animal.save()
    messages.success(request,'Animal verified successfully')
    return redirect('doctor_verify_animals')


@login_required()
def rejectAnimal(request):
    
    if request.method == 'POST':
        id = request.POST['id']
        animal = Animals.objects.get(pk=id)
        reason = request.POST['reason']

        if reason.isdigit():
            return render(request,'verify animals.html',{'error':True,'unverified_animals':request.session.get('unverified_animals_count')})
        else:
            animal.status = -2
            animal.save()
            messages.success(request,'Animal rejected successfully')
            return redirect('doctor_verify_animals')


@login_required()
def viewAnimalHealth(request):
    animals = Animals.objects.filter(status=1)
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    return render(request,'viewanimalhealth.html',{'animals':animals,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def changeAnimalHealthStatus(request,id):
    animal = Animals.objects.get(pk=id)
    
    if animal.health_status == 'healthy':
        animal.health_status = 'sick'
    else:
        animal.health_status = 'healthy'
    
    animal.save()

    messages.success(request,'Animal health status changed successfully')
    return redirect('doctor_view_health_status')


@login_required()
def sickAnimalList(request):
    sick_animals = sickness_details.objects.all()
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    return render(request,'sick animals.html',{'sickAnimals':sick_animals,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def addSickness(request):
    sicknessForm = SicknessForm()
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()

    if request.method == 'GET':
        return render(request,'add sickness details.html',{'form':sicknessForm,'unverified_animals':request.session.get('unverified_animals_count')})

    elif request.method == 'POST':
        form = SicknessForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 'sick'
            animal = Animals.objects.get(pk=obj.animal.id)
            animal.health_status = 'sick'
            # print(animal.health_status)
            animal.save()
            obj.save()
            messages.success(request,'Sickness added successfully')
            return redirect('doctor_manage_sick_animals')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'add sickness details.html',{'form':form,'unverified_animals':request.session.get('unverified_animals_count')})
    else:
        return render(request,'add sickness details.html',{'form':sicknessForm,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def markCured(request,id):
    sickAanimal = sickness_details.objects.get(pk=id)
    sickAanimal.status = 'cured'
    animal = Animals.objects.get(pk=sickAanimal.animal.id)
    animal.health_status = 'healthy'
    # print(animal)
    animal.save()
    sickAanimal.save()
    messages.success(request,'Animal marked as cured')
    return redirect('doctor_manage_sick_animals')


@login_required()
def viewMedicineConsumption(request,id):
    consumptionObj = ConsumptionDetails.objects.filter(sick_animal=id)
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    return render(request,'doctor view consumption.html',{'consumption':consumptionObj,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def medicineList(request):
    medicines = Medicines.objects.all()
    medicineForm = MedicineForm()
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    
    if request.method == 'GET':
        return render(request,'view medicines.html',{'medicines':medicines,'form':medicineForm,'unverified_animals':request.session.get('unverified_animals_count')})
    elif request.method == 'POST':
        form = MedicineForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,'Medicine added successfully')
            return redirect('doctor_manage_medicines')
        else:
            return render(request,"view medicines.html",{'form':form,'medicines':medicines,'error':True,'unverified_animals':request.session.get('unverified_animals_count')})
    else:
        return render(request,'view medicines.html',{'form':medicineForm,'medicines':medicines,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()    
def updateStock(request,id):
    medicines = Medicines.objects.all()
    medicineForm = MedicineForm()
    medicine = Medicines.objects.get(pk=id)
    medicine_stock = request.POST['stock']
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()

    if int(medicine_stock) < 0:
        messages.error(request,'Invalid stock entered')
        return render(request,"view medicines.html",{'form':medicineForm,'medicines':medicines,'update_error':True,'unverified_animals':request.session.get('unverified_animals_count')})
    else:
        medicine.stock = medicine_stock
        medicine.save()
        messages.success(request,'Medicine stock updated successfully')
        return redirect('doctor_manage_medicines')


@login_required()
def deleteMedicine(request,id):
    medicine = Medicines.objects.get(pk=id)
    medicine.delete()
    messages.success(request,'Medicine deleted successfully')
    return redirect('doctor_manage_medicines')


@login_required()
def viewAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    return render(request,'viewanimaldetail.html',{'animal':animal,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def viewDeathDetails(request):
    animals = Animals.objects.filter(Q(status=1) | Q(status=0))
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()
    return render(request,'death details.html',{'animals':animals,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def updateDeathDetails(request,id):
    animal = Animals.objects.get(pk=id)
    deathForm = DeathForm(instance=animal)
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()

    if request.method == 'GET':
        return render(request,'add death details.html',{'form':deathForm,'animal':animal,'unverified_animals':request.session.get('unverified_animals_count')})

    elif request.method == 'POST':
        form = DeathForm(request.POST,instance = animal)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 0
            obj.save()
            messages.success(request,'death details added successfully')
            return redirect('doctor_manage_animal_death')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'add death details.html',{'form':form,'animal':animal,'unverified_animals':request.session.get('unverified_animals_count')})
    else:
        return render(request,'add death details.html',{'form':deathForm,'animal':animal,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def viewComplaints(request):
    complaints = Complaints.objects.filter(uid = request.user.id)
    recipient = Users.objects.filter(usertype__in = ['curator','director'])
    # print(recipient[0].usertype)
    complaintForm = ComplaintForm()
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()

    if request.method == 'GET':
        return render(request,'doctor view complaint.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient,'unverified_animals':request.session.get('unverified_animals_count')})

    elif request.method == 'POST':
        recipient = request.POST['recipient']
        form = ComplaintForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = Users.objects.get(pk=request.user.id)
            obj.rid = Staffs.objects.get(user=recipient)
            obj.save()
            messages.success(request,'Complaint registered successfully')
            return redirect('doctor_view_complaints')
        else:
            return render(request,"doctor view complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True,'unverified_animals':request.session.get('unverified_animals_count')})
    else:
        return render(request,'doctor view complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    messages.success(request,'Complaint deleted successfully')
    return redirect('doctor_view_complaints')


@login_required()
def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()

    if request.method == 'GET':
        return render(request,'doctor update profile.html',{'form':profileForm,'imageform':profileImageForm,'unverified_animals':request.session.get('unverified_animals_count')})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('doctor_view_profile')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'doctor update profile.html',{'form':form,'unverified_animals':request.session.get('unverified_animals_count')})
    else:
        return render(request,'doctor update profile.html',{'form':profileForm,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def updateProfileImage(request):
    profileImageForm = ProfileImageForm(instance=request.user)
    request.session['unverified_animals_count'] = Animals.objects.filter(status = -1).count()

    if request.method == 'POST':
        form = ProfileImageForm(request.POST,request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile image updated successfully')
            return redirect('doctor_view_profile')
        else:
            return render(request,'doctor update profile.html',{'form':form,'imageform':profileImageForm,'error':True,'unverified_animals':request.session.get('unverified_animals_count')})


@login_required()
def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('doctor_view_profile')


@login_required()
def changePassword(request):
    currentPassword = request.POST['password']
    newPassword = request.POST['newpassword']
    renewPassword = request.POST['renewpassword']

    user = authenticate(username = request.user.username , password = currentPassword)

    if user:
        if newPassword == renewPassword:
            request.user.set_password(newPassword)
            request.user.save()
            messages.success(request,'Password changed successfully!')
            return redirect('login_user')
        else:
            messages.error(request,'new and reentered passwords mismatch!')
            return redirect('doctor_view_profile')
    else:
        messages.error(request,'current password is wrong!')
        return redirect('doctor_view_profile')
