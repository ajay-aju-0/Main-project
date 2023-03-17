from django.shortcuts import render,redirect
from accounts.models import *
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