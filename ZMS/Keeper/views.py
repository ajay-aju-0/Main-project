from django.shortcuts import render,redirect
from accounts.models import *
from Visitor.forms import *
from Director.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate
# Create your views here.

def loadKeeperHome(request):
    return render(request,'keeperhome.html')

def viewAnimalHealthStatus(request):
    animals = Animals.objects.all()
    return render(request,'viewanimalhealthstatus.html',{'animals':animals})

def showAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    return render(request,'keeperviewanimaldetail.html',{'animal':animal})

def changeAnimalHealthStatus(request,id):
    animal = Animals.objects.get(pk=id)
    
    if animal.health_status == 'healthy':
        animal.health_status = 'sick'
    else:
        animal.health_status = 'healthy'
    
    animal.save()
    return redirect('keeper_view_animal_health_status')


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
            obj.rid = Staffs.objects.get(user=recipient)
            obj.save()
            return redirect('keeper_view_complaint')
        else:
            return render(request,"keeper view complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True})
    else:
        return render(request,'keeper view complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})

def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    return redirect('keeper_view_complaint')


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

def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('keeper_view_profile')

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