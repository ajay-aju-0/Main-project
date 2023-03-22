from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.db.models import Count
from accounts.forms import *
from accounts.models import *
from .forms import *
from datetime import date
from django.contrib.auth import authenticate



# Create your views here.

def loadDirectorHome(request):
    return render(request,'directorHome.html')

def viewZooDetails(request):
    details = ZooDetails.objects.get(pk=1)
    detailsForm = ZooDetailsForm(instance=details)
    if request.method == 'GET':
        return render(request,'zoo details.html',{'form':detailsForm,'details':details})
    elif request.method == 'POST':
        form = ZooDetailsForm(request.POST,instance=details)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.current_animal_occupancy = Animals.objects.filter(status=1).count()
            obj.enclosure_types = Enclosures.objects.all().count()
            obj.save()
            messages.success(request,"Zoo details Updated successfully")
            return redirect('director_view_zoo_details')
        else:
            # messages.error(request,'error while updating form')
            return render(request,'zoo details.html',{'form':form,'details':details})
    else:
        return render(request,'zoo details.html',{'form':detailsForm,'details':details})


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


def viewTicketSales(request):
    tickets = Ticket.objects.values('tdate').annotate(tcount=Count('tdate')).order_by()
    for i in tickets:
        print(i.get('tdate'),i.get('tcount'))
    return render(request,'view ticket sales.html',{'tickets':tickets})


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

def showAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    return render(request,'viewanimaldetails.html',{'animal':animal})

def showPurchases(request):
    purchase = Purchase.objects.all()
    return render(request,'view purchase history.html',{'purchase':purchase})

def sponserList(request):
    sponsers = SponserDetails.objects.all()
    return render(request,"manage sponsers.html",{'sponsers':sponsers})

def addSponser(request):
    sponserForm = SponserForm()
    sponseredAnimalsForm = SponseredAnimalForm()
    current_date = date.today()

    if request.method == 'GET':
            return render(request,'add sponser.html',{'form1':sponserForm,'form2':sponseredAnimalsForm,'currentDate':current_date})
    
    elif request.method == 'POST':
        form1 = SponserForm(request.POST)
        form2 = SponseredAnimalForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            if SponserDetails.objects.filter(name=request.POST['name'],address=request.POST['address'],phone=request.POST['phone'],email=request.POST['email'],stype=request.POST['stype'],amount=request.POST['amount'],sdate=request.POST['sdate'],edate=request.POST['edate']).exists():
                sponserObj = SponserDetails.objects.get(name=request.POST['name'],address=request.POST['address'],phone=request.POST['phone'],email=request.POST['email'],stype=request.POST['stype'],amount=request.POST['amount'],sdate=request.POST['sdate'],edate=request.POST['edate'])
            else: 
                form1.save()
                sponserObj = SponserDetails.objects.get(name=request.POST['name'],address=request.POST['address'],phone=request.POST['phone'],email=request.POST['email'],stype=request.POST['stype'],amount=request.POST['amount'],sdate=request.POST['sdate'],edate=request.POST['edate'])
                
            obj = form2.save(commit=False)
            obj.sponser = sponserObj
            obj.save()
            messages.success(request,"Sponser registered successfully")
            return redirect("director_manage_sponsers")
        else:
            messages.error(request,"error while submitting form")
            return render(request,'add sponser.html',{'form1':form1,'form2':form2})
    else:
        return redirect('director_manage_sponsers')

def updateSponser(request,id):
    sponser = SponserDetails.objects.get(pk=id)
    sponserForm = SponserForm(instance=sponser)
    if request.method == 'GET':
        return render(request,'update sponser.html',{'form':sponserForm})
    
    elif request.method == 'POST':
        form = SponserForm(request.POST,instance=sponser)

        if form.is_valid():
            form.save()
            messages.success(request,'sponser updated successfully')
            return redirect('director_manage_sponsers')
        else:
            messages.error(request,"error while submitting form")
            return render(request,'update sponser.html',{'form1':form})
    else:
        return redirect('director_manage_sponsers')

def showSponseredAnimals(request,id):
    animals = SponseredAnimals.objects.filter(sponser = id)
    return render(request,'sponsered animal details.html',{'animals':animals})

def deleteSponseredAnimal(request,id):
    animal = SponseredAnimals.objects.get(pk = id)
    animal.delete()
    messages.success(request,"sponsered animal deleted successfully!")
    return redirect('director_manage_sponsers')

def deleteSponser(request,id):
    sponser = SponserDetails.objects.get(pk=id)
    sponser.delete()
    return redirect('director_manage_sponsers')

def showFeedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request,'director view feedbacks.html',{'feedbacks':feedbacks})

def viewComplaints(request):
    complaints = Complaints.objects.filter(rid = Staffs.objects.get(user=request.user.id))

    if request.method == 'GET':
        return render(request,'director view complaints.html',{'complaints':complaints})
    
    elif request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        reply = request.POST.get('reply')
        # print(complaint_id,reply)

        complaint_obj = Complaints.objects.get(pk=complaint_id)
        complaint_obj.reply = reply
        complaint_obj.save()
        return redirect('director_view_complaints')
    else:
        return render(request,'director view complaints.html',{'complaints':complaints})


def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'GET':
        return render(request,'director update profile.html',{'form':profileForm,'imageform':profileImageForm})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('director_view_profile')
        else:
            print('invalid')
            print(form.errors)
            messages.error(request,'Error while submitting form')
            return render(request,'director update profile.html',{'form':form})
    else:
        print('nothing')
        return render(request,'director update profile.html',{'form':profileForm})

def updateProfileImage(request):
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST,request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile image updated successfully')
            return redirect('director_view_profile')
        else:
            return render(request,'director update profile.html',{'form':form,'imageform':profileImageForm,'error':True})

def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('director_view_profile')

def changePassword(request):
    # userObj = Users.objects.get(pk=request.user.id)
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
            return redirect('director_view_profile')
    else:
        messages.error(request,'current password is wrong!')
        return redirect('director_view_profile')
    

    print(currentPassword,newPassword,renewPassword)
    return redirect('director_view_profile')
