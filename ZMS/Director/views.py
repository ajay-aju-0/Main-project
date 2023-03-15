from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from accounts.forms import *
from .forms import *
from datetime import date


# Create your views here.

def loadDirectorHome(request):
    return render(request,'directorHome.html')


def staffList(request):
    staffObj = Staffs.objects.all()
    return render(request,'view staffs.html',{'staffs':staffObj})


def addCurator(request):
    userForm = RegistrationForm(initial={'usertype':'curator'})
    staffForm = CuratorForm() 
    if request.method == 'GET':
        return render(request,'add curator.html',{'form1':userForm,'form2':staffForm})

    elif request.method == 'POST':
        form1 = RegistrationForm(request.POST,request.FILES)
        form2 = CuratorForm(request.POST)
        passw = request.POST['password']
        if form1.is_valid() and form2.is_valid():
            obj1 = form1.save(commit=False)
            obj2 = form2.save(commit=False)
            obj1.set_password(passw)
            obj2.desig = "curator"
            obj2.user = obj1
            obj1.save()
            obj2.save()
            messages.success(request,"Curator registered successfully")
            return redirect('director_manage_staff')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'add curator.html',{'form1':form1,'form2':form2,'staff':True})
    else:
        return render(request,'add curator.html',{'form1':userForm,'form2':staffForm})


def updateStaff(request,id):
    staff = Staffs.objects.get(user=id)
    uname = Users.objects.get(pk=id)
    if request.method == 'GET':
        context = {}
        context['form'] = StaffForm(instance=staff)
        context['uname'] = uname
        return render(request, 'updatestaff.html', context)
    
    elif request.method == 'POST':
        form = StaffForm(request.POST,instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request,"Staff Updated successfully")
            return redirect('director_manage_staff')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'update staff.html',{'form':form,'staff':True})
    else:
        return redirect('director_manage_staff')


def changeStaffStatus(request,id):
    staff = Users.objects.get(pk=id)
    if staff.is_active == 0:
        staff.is_active = 1
    else:
        staff.is_active = 0
    staff.save()
    return redirect('director_manage_staff')


def manageTicketRates(request):
    rateForm = TicketRateForm()
    rates = TicketRate.objects.all()
    if request.method == 'GET':
        return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})

    elif request.method == 'POST':
        form = TicketRateForm(request.POST)
        # ttype = request.POST.get('type')
        if form.is_valid():
            form.save()
            messages.success(request,"Ticket catagory added successfully")
            return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})
        else:
            # messages.error(request,"error while submitting form")
            return render(request,"manageticketrates.html",{'form':form,'rates':rates,'error':True})
    else:
        return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})


def deleteTicketCatagory(request,id):
    catagory = TicketRate.objects.get(pk=id)
    catagory.delete()
    return redirect('director_manage_ticket_rate')

def UpdateTicketCatagory(request,id):
    rate = TicketRate.objects.get(pk=id)
    rates = TicketRate.objects.all()
    # catagory = TicketRateForm(instance=rate)
    rateForm = UpdateTicketRateForm()
    # print(rate,catagory)
    if request.method == 'POST':
        ttype = request.POST.get('type')
        # print(ttype,trate) 
        # print(ttype.isdigit())
        form = UpdateTicketRateForm(request.POST,instance=rate)
        if form.is_valid():
            form.save()
            messages.success(request,"Ticket catagory Updated successfully")
            return redirect('director_manage_ticket_rate')
        else:
            # messages.error(request,'error while updating form')
            return render(request,'manageticketrates.html',{'update_form':form,'form':rateForm,'rates':rates,'error':True})
    else:
        return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})


def vacancyList(request):
    vacancy = JobVacancy.objects.all()
    return render(request,'manage vacancy.html',{'vacancies':vacancy})

def addVacancy(request):
    vacancyForm = VacancyForm()
    if request.method == 'GET':
        return render(request,'add vacancy.html',{'form':vacancyForm})

    elif request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Vacancy added successfully")
            return redirect('director_manage_vacancy')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'add vacancy.html',{'form':form})
    else:
        return render(request,'add vacancy.html',{'form':vacancyForm})

def updateVacancy(request,id):
    vacancy = JobVacancy.objects.get(pk=id)
    if request.method == 'GET':
        vacancy_form = VacancyForm(instance=vacancy)
        return render(request,'update vacancy.html',{'form':vacancy_form})
    elif request.method == 'POST':
        form = VacancyForm(request.POST,instance=vacancy)
        if form.is_valid():
            form.save()
            messages.success(request,'Vacancy updated successfully')
            return redirect('director_manage_vacancy')
        else:
            messages.error(request,"error while submitting form")
            return render(request,'update vacancy.html',{'form':form})
    else:
        return redirect('director_manage_vacancy')

def closeVacancy(request,id):
    catagory = JobVacancy.objects.get(pk=id)
    vacancy = JobVacancy.objects.all()
    catagory.vstatus = "closed"
    catagory.save()
    return render(request,'manage vacancy.html',{'message':True,'vacancies':vacancy})

def visitorList(request):
    visitors = Users.objects.filter(usertype="visitor")
    return render(request,"visitor list.html",{'visitors':visitors})

def showZooTime(request):
    zoo_time = ZooTimings.objects.all()
    timeForm = ZooTimeForm()
    if request.method == 'GET':
        return render(request,'view zoo time.html',{'time':zoo_time,'timeform':timeForm})

    elif request.method == 'POST':
        id = request.POST.get('id')
        zt_obj = ZooTimings.objects.get(id=id)
        open = request.POST['open time']
        close = request.POST['close time']
        # print(id,zt_obj.day,open,close)
        zt_obj.open_time = open
        zt_obj.close_time = close
        zt_obj.save()
        return redirect("director_manage_zoo_time")

    else:
        return render(request,'view zoo time.html',{'time':zoo_time,'timeform':timeForm})

def eventsList(request):
    events = Events.objects.all()
    current_date = date.today()
    for event in events:
        print(event.estart,event.eend)
        if event.estart > current_date:
            event.estatus = "upcoming"
        elif event.estart <= current_date <= event.eend:
            event.estatus = "ongoing"
        else:
            event.estatus = "finished"
        event.save()
    
    return render(request,'manage events.html',{'events':events})

def addEvents(request):
    eventForm = EventForm()
    
    if request.method == 'GET':
        return render(request,'add events.html',{'form':eventForm})

    elif request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.estatus = "upcoming"
            obj.save()
            messages.success(request,"Event added successfully")
            return redirect("director_manage_events")
        else:
            messages.error(request,"Error in form submission!")
            return render(request,"add events.html",{'form':form})
    else:
        return render(request,'add events.html',{'form':eventForm})

def updateEvents(request,id):
    event = Events.objects.get(pk=id)

    if request.method == 'GET':
        eventForm = UpdateEventForm(instance=event)
        return render(request,"update events.html",{'form':eventForm})

    elif request.method == 'POST':
        form = UpdateEventForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,'Event updated successfully')
            return redirect('director_manage_events')
        else:
            messages.error(request,"error while submitting form")
            return render(request,'update events.html',{'form':form})
    else:
        return redirect('director_manage_events')

def enclosureList(request):
    enclosures = Enclosures.objects.all()
    return render(request,"enclosures list.html",{'enclosures':enclosures})

def animalList(request):
    animals = Animals.objects.all()
    return render(request,'view animal.html',{'animals':animals})

def showPurchases(request):
    purchase = Purchase.objects.all()
    return render(request,'view purchase history.html',{'purchase':purchase})

def sponserList(request):
    sponsers = SponserDetails.objects.all()
    return render(request,"manage sponsers.html",{'sponsers':sponsers})

def addSponser(request):
    sponserForm = SponserForm()
    sponseredAnimalsForm = SponseredAnimalForm()

    if request.method == 'GET':
            return render(request,'add sponser.html',{'form1':sponserForm,'form2':sponseredAnimalsForm})
