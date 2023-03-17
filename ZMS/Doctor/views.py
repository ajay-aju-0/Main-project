from django.shortcuts import render,redirect
from accounts.models import *
from .forms import *
from django.contrib import messages

# Create your views here.

def loadDoctorHome(request):
    return render(request,'doctorHome.html')

def animalVerification(request):
    animals = Animals.objects.all()
    return render(request,'verify animals.html',{'animals':animals})

def verifyAnimal(request,id):
    animal = Animals.objects.get(pk=id)
    animal.status = 1
    animal.save()
    return redirect('doctor_verify_animals')

def viewAnimalHealth(request):
    animals = Animals.objects.all()
    if request.method == 'GET':
        return render(request,'viewanimalhealth.html',{'animals':animals})

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
    return render(request,'sick animals.html',{'sickAnimals':sick_animals})

def addSickness(request):
    sicknessForm = SicknessForm()
    if request.method == 'GET':
        return render(request,'add sickness details.html',{'form':sicknessForm})

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
            return render(request,'add sickness details.html',{'form':form})
    else:
        return render(request,'add sickness details.html',{'form':sicknessForm})

def markCured(request,id):
    animal = sickness_details.objects.get(pk=id)
    animal.status = 'cured'
    animal.save()
    return redirect('doctor_manage_sick_animals')


def medicineList(request):
    medicines = Medicines.objects.all()
    medicineForm = MedicineForm()
    if request.method == 'GET':
        return render(request,'view medicines.html',{'medicines':medicines,'form':medicineForm})
    elif request.method == 'POST':
        form = MedicineForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,'Medicine added successfully')
            return render(request,'view medicines.html',{'form':medicineForm,'medicines':medicines})
        else:
            return render(request,"view medicines.html",{'form':medicineForm,'medicines':medicines,'error':True})
    else:
        return render(request,'view medicines.html',{'form':medicineForm,'medicines':medicines})

            
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
    return render(request,'viewanimaldetail.html',{'animal':animal})

def viewDeathDetails(request):
    animals = Animals.objects.all()
    return render(request,'death details.html',{'animals':animals})

def updateDeathDetails(request,id):
    animal = Animals.objects.get(pk=id)
    deathForm = DeathForm(instance=animal)
    if request.method == 'GET':
        return render(request,'add death details.html',{'form':deathForm,'animal':animal})

    elif request.method == 'POST':
        form = DeathForm(request.POST,instance = animal)
        if form.is_valid():
            form.save()
            messages.success(request,'death details added successfully')
            return redirect('doctor_manage_animal_death')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'add death details.html',{'form':form,'animal':animal})
    else:
        return render(request,'add death details.html',{'form':deathForm,'animal':animal})

            