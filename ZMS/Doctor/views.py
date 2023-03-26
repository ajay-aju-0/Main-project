from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from .forms import *
from Visitor.forms import ComplaintForm
from Director.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate


# Create your views here.

def loadDoctorHome(request):
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    return render(request,'doctorHome.html',{'unverified_animals':unverified_animals_count})

def animalVerification(request):
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    animals = Animals.objects.filter(status = -1)
    return render(request,'verify animals.html',{'animals':animals,'unverified_animals':unverified_animals_count})

def verifyAnimal(request,id):
    animal = Animals.objects.get(pk=id)
    animal.status = 1
    animal.save()
    return redirect('doctor_verify_animals')

def rejectAnimal(request):
    if request.method == 'POST':
        id = request.POST['id']
        animal = Animals.objects.get(pk=id)
        animal.reason = request.POST['reason']
        animal.status = -2
        animal.save()
    return redirect('doctor_verify_animals')

def viewAnimalHealth(request):
    animals = Animals.objects.filter(status=1)
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    return render(request,'viewanimalhealth.html',{'animals':animals,'unverified_animals':unverified_animals_count})

def changeAnimalHealthStatus(request,id):
    animal = Animals.objects.get(pk=id)
    
    if animal.health_status == 'healthy':
        animal.health_status = 'sick'
    else:
        animal.health_status = 'healthy'
    
    animal.save()
    return redirect('doctor_view_health_status')

def sickAnimalList(request):
    sick_animals = sickness_details.objects.all()
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    return render(request,'sick animals.html',{'sickAnimals':sick_animals,'unverified_animals':unverified_animals_count})

def addSickness(request):
    sicknessForm = SicknessForm()
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    if request.method == 'GET':
        return render(request,'add sickness details.html',{'form':sicknessForm,'unverified_animals':unverified_animals_count})

    elif request.method == 'POST':
        form = SicknessForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 'sick'
            obj.save()
            messages.success(request,'Sickness added successfully')
            return redirect('doctor_manage_sick_animals')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'add sickness details.html',{'form':form,'unverified_animals':unverified_animals_count})
    else:
        return render(request,'add sickness details.html',{'form':sicknessForm,'unverified_animals':unverified_animals_count})

def markCured(request,id):
    animal = sickness_details.objects.get(pk=id)
    animal.status = 'cured'
    animal.save()
    return redirect('doctor_manage_sick_animals')


def medicineList(request):
    medicines = Medicines.objects.all()
    medicineForm = MedicineForm()
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    if request.method == 'GET':
        return render(request,'view medicines.html',{'medicines':medicines,'form':medicineForm,'unverified_animals':unverified_animals_count})
    elif request.method == 'POST':
        form = MedicineForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,'Medicine added successfully')
            return render(request,'view medicines.html',{'form':medicineForm,'medicines':medicines,'unverified_animals':unverified_animals_count})
        else:
            return render(request,"view medicines.html",{'form':medicineForm,'medicines':medicines,'error':True,'unverified_animals':unverified_animals_count})
    else:
        return render(request,'view medicines.html',{'form':medicineForm,'medicines':medicines,'unverified_animals':unverified_animals_count})

            
def updateStock(request,id):
    medicine = Medicines.objects.get(pk=id)
    medicine.stock = request.POST['stock']
    medicine.save()
    return redirect('doctor_manage_medicines')

def deleteMedicine(request,id):
    medicine = Medicines.objects.get(pk=id)
    medicine.delete()
    return redirect('doctor_manage_medicines')

def viewAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    return render(request,'viewanimaldetail.html',{'animal':animal,'unverified_animals':unverified_animals_count})

def viewDeathDetails(request):
    animals = Animals.objects.all()
    unverified_animals_count = Animals.objects.filter(status = -1).count()
    return render(request,'death details.html',{'animals':animals,'unverified_animals':unverified_animals_count})

def updateDeathDetails(request,id):
    animal = Animals.objects.get(pk=id)
    deathForm = DeathForm(instance=animal)
    unverified_animals_count = Animals.objects.filter(status = -1).count()

    if request.method == 'GET':
        return render(request,'add death details.html',{'form':deathForm,'animal':animal,'unverified_animals':unverified_animals_count})

    elif request.method == 'POST':
        form = DeathForm(request.POST,instance = animal)
        if form.is_valid():
            form.save()
            messages.success(request,'death details added successfully')
            return redirect('doctor_manage_animal_death')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'add death details.html',{'form':form,'animal':animal,'unverified_animals':unverified_animals_count})
    else:
        return render(request,'add death details.html',{'form':deathForm,'animal':animal,'unverified_animals':unverified_animals_count})

def viewComplaints(request):
    complaints = Complaints.objects.filter(uid = request.user.id)
    recipient = Users.objects.filter(usertype__in = ['curator','director'])
    # print(recipient[0].usertype)
    complaintForm = ComplaintForm()
    unverified_animals_count = Animals.objects.filter(status = -1).count()


    if request.method == 'GET':
        return render(request,'doctor view complaint.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient,'unverified_animals':unverified_animals_count})

    elif request.method == 'POST':
        recipient = request.POST['recipient']
        form = ComplaintForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = Users.objects.get(pk=request.user.id)
            obj.rid = Staffs.objects.get(user=recipient)
            obj.save()
            return redirect('doctor_view_complaints')
        else:
            return render(request,"doctor view complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True,'unverified_animals':unverified_animals_count})
    else:
        return render(request,'doctor view complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient,'unverified_animals':unverified_animals_count})

def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    return redirect('doctor_view_complaints')

def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)
    unverified_animals_count = Animals.objects.filter(status = -1).count()

    if request.method == 'GET':
        return render(request,'doctor update profile.html',{'form':profileForm,'imageform':profileImageForm,'unverified_animals':unverified_animals_count})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('doctor_view_profile')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'doctor update profile.html',{'form':form,'unverified_animals':unverified_animals_count})
    else:
        return render(request,'doctor update profile.html',{'form':profileForm,'unverified_animals':unverified_animals_count})

def updateProfileImage(request):
    profileImageForm = ProfileImageForm(instance=request.user)
    unverified_animals_count = Animals.objects.filter(status = -1).count()

    if request.method == 'POST':
        form = ProfileImageForm(request.POST,request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile image updated successfully')
            return redirect('doctor_view_profile')
        else:
            return render(request,'doctor update profile.html',{'form':form,'imageform':profileImageForm,'error':True,'unverified_animals':unverified_animals_count})

def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('doctor_view_profile')

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