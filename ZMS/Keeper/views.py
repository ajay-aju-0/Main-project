from django.shortcuts import render,redirect
from accounts.models import *
from Visitor.forms import *
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