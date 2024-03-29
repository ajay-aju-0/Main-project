from django.shortcuts import render,redirect
from django.db.models import Count,Q
from accounts.models import *
from Visitor.forms import *
from Director.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required()
def loadKeeperHome(request):
    animal = Animals.objects.filter(Q(status = 1) & Q(caretaker = Staffs.objects.get(user=request.user.id).id)).count()
    guided = Ticket.objects.filter(Q(reporting_date__year = date.today().year) & Q(reporting_date__month = date.today().month) & Q(Guide = Staffs.objects.get(user=request.user.id)) ).count()
    
    context = {
        'animal':animal,
        'guide':guided
    }

    return render(request,'keeperhome.html',context)


@login_required()
def viewAnimalHealthStatus(request):
    animals = Animals.objects.filter(Q(status = 1) & Q(caretaker = request.user.id))
    return render(request,'viewanimalhealthstatus.html',{'animals':animals})


@login_required()
def showAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    return render(request,'keeperviewanimaldetail.html',{'animal':animal})


@login_required()
def changeAnimalHealthStatus(request,id):
    animal = Animals.objects.get(pk=id)
    
    if animal.health_status == 'healthy':
        animal.health_status = 'sick'
    else:
        animal.health_status = 'healthy'
    
    animal.save()
    messages.success(request,'Health status changed successfully')
    return redirect('keeper_view_animal_health_status')


@login_required()
def viewSickAnimals(request):
    sick_animals = []
    sick_animals_list = []
    j=0
    for i in Animals.objects.filter(caretaker = request.user.id):
        if sickness_details.objects.filter(animal = i.id).exists():
            sick_animals.append(sickness_details.objects.filter(animal = i.id))
    # print(sick_animals)
    for j in range(len(sick_animals)):
        sick_animals_list.append(sick_animals[j][0])

    # print(sick_animals_list)
    return render(request,'keeper view sick animals.html',{'sickAnimals':sick_animals_list})


@login_required()
def updateConsumption(request,id,medicine):
    consumptionForm = ConsumptionForm()
    animal = sickness_details.objects.get(pk=id)

    if request.method == 'GET':
        return render(request,'update consumption.html',{'form':consumptionForm,'animal':animal.animal,'medicine':medicine})

    if request.method == 'POST':
        form = ConsumptionForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.sick_animal = animal
            
            medicine_stock = Medicines.objects.get(medicine=medicine)
            medicine_stock.stock = medicine_stock.stock - obj.dose
            
            if medicine_stock.stock >= 0:
                medicine_stock.save()
                obj.save()

                messages.success(request,'Consumption details added successfully')
                return redirect('keeper_manage_sick_animals')
            else:
                messages.error(request,'This much dose is not available!')
                return render(request,'update consumption.html',{'form':form,'animal':animal.animal,'medicine':medicine})

        else:
            messages.error(request,'Something went wrong!')
            return render(request,'update consumption.html',{'form':form,'animal':animal.animal,'medicine':medicine})

    else:
        return render(request,'update consumption.html',{'form':consumptionForm,'animal':animal.animal,'medicine':medicine})


@login_required()
def viewMedicineConsumption(request,id):
    consumptionObj = ConsumptionDetails.objects.filter(sick_animal=id)
    return render(request,'view consumption.html',{'consumption':consumptionObj})


@login_required()
def viewGuidingSlots(request):
    guiding_slots = Ticket.objects.filter(Guide = request.user.id)
    current_date = datetime.today().date()
    return render(request,'guiding slots.html',{'slots':guiding_slots,'current':current_date})


@login_required()
def viewComplaints(request):
    complaints = Complaints.objects.filter(uid = request.user.id)
    recipient = Users.objects.filter(usertype__in = ['curator','director'])
    # print(recipient[0].usertype)
    complaintForm = ComplaintForm()

    if request.method == 'GET':
        return render(request,'keeper view complaint.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})

    elif request.method == 'POST':
        recipient = request.POST['recipient']
        form = ComplaintForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = Users.objects.get(pk=request.user.id)
            obj.rid = Users.objects.get(pk=recipient)
            obj.save()
            messages.success(request,'Complaint registered successfully')
            return redirect('keeper_view_complaint')
        else:
            return render(request,"keeper view complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True})
    else:
        return render(request,'keeper view complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})


@login_required()
def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    messages.success(request,'Complaint deleted successfully')
    return redirect('keeper_view_complaint')


@login_required()
def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'GET':
        return render(request,'keeper update profile.html',{'form':profileForm,'imageform':profileImageForm})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('keeper_view_profile')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'keeper update profile.html',{'form':form})
    else:
        return render(request,'keeper update profile.html',{'form':profileForm})


@login_required()
def updateProfileImage(request):
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST,request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile image updated successfully')
            return redirect('keeper_view_profile')
        else:
            return render(request,'keeper update profile.html',{'form':form,'imageform':profileImageForm,'error':True})


@login_required()
def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('keeper_view_profile')


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
            return redirect('keeper_view_profile')
    else:
        messages.error(request,'current password is wrong!')
        return redirect('keeper_view_profile')
