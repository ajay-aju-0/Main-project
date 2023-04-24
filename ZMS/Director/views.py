from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count,Q
from accounts.forms import *
from accounts.models import *
from .forms import *
from datetime import date
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


@login_required()
def loadDirectorHome(request):
    visitor_obj = Users.objects.filter(usertype = 'visitor',is_active = True).values('date_joined')
    staff_obj = Users.objects.exclude(Q(usertype = 'director') | Q(usertype ='visitor')).filter(is_active = True).values('date_joined')
    animal_obj = Animals.objects.filter(status = 1).values('date_joined')
    vacancy_obj = JobVacancy.objects.filter().values('issue_date')
    ticket_obj = Ticket.objects.filter().values('tdate')
    ticket_revenue_obj = Ticket.objects.filter().values('tdate','total')
    sponser_revenue_obj = SponseredAnimals.objects.filter().values('sdate','amount')

    visitors = []
    staffs = []
    animals = []
    vacancy = []
    ticket = []
    ticket_revenue = []
    sponser_revenue = []

    for i in visitor_obj:
        if i['date_joined'].year == date.today().year:
            visitors.append(i)

    for j in staff_obj:
        if j['date_joined'].year == date.today().year:
            staffs.append(j)

    for k in animal_obj:
        if k['date_joined'].year == date.today().year:
            animals.append(k)

    for l in vacancy_obj:
        if l['issue_date'].year == date.today().year:
            vacancy.append(l)

    for m in ticket_obj:
        if m['tdate'].year == date.today().year:
            ticket.append(m)

    for n in ticket_revenue_obj:
        if n['tdate'].year == date.today().year:
            ticket_revenue.append(n['total'])

    for p in sponser_revenue_obj:
        if p['sdate'].year == date.today().year:
            sponser_revenue.append(p['amount'])


    total_revenue = sum(ticket_revenue) + sum(sponser_revenue)


    tickets = Ticket.objects.values('tdate').annotate(tcount=Count('tdate')).order_by()
    visitors_count_obj = Users.objects.filter(usertype = 'visitor',is_active = True).values('date_joined').annotate(vcount=Count('date_joined')).order_by()

    sales = [0] * 12
    visitors_count = [0] * 12
    ticket_revenue_list = [0] * 12
    sponser_revenue_list = [0] * 12
    total_revenue_list = [0] * 12


    for i in tickets:
        if i['tdate'].year == date.today().year:
            for j in range(12):
                if j == i['tdate'].month - 1:
                    sales[j] += i['tcount']

    
    for i in visitors_count_obj:
        if i['date_joined'].year == date.today().year:
            for j in range(12):
                if j == i['date_joined'].month -1:
                    visitors_count[j] += i['vcount']


    for t in ticket_revenue_obj:
        if t['tdate'].year == date.today().year:
            for j in range(12):
                if j == t['tdate'].month -1:
                    ticket_revenue_list[j] += t['total']


    for s in sponser_revenue_obj:
        if s['sdate'].year == date.today().year:
            for j in range(12):
                if j == s['sdate'].month -1:
                    sponser_revenue_list[j] += s['sdate']

    for i in range(12):
        total_revenue_list[i] = ticket_revenue_list[i] + sponser_revenue_list[i]

    
    
    context ={
        'visitors':len(visitors),
        'staffs':len(staffs),
        'animals':len(animals),
        'vacancy':len(vacancy),
        'ticket':len(ticket),
        'revenue':total_revenue,
        'sales':sales,
        'visitor_count':visitors_count,
        'total_revenue':total_revenue_list
    }

    return render(request,'directorHome.html',context)


@login_required()
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
            messages.error(request,'error while updating form')
            return render(request,'zoo details.html',{'form':form,'details':details,'error':True})
    else:
        return render(request,'zoo details.html',{'form':detailsForm,'details':details})


@login_required()
def staffList(request):
    staffObj = Staffs.objects.exclude(desig = 'director')
    return render(request,'view staffs.html',{'staffs':staffObj})


@login_required()
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


@login_required()
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


@login_required()
def changeStaffStatus(request,id):
    staff = Users.objects.get(pk=id)
    if staff.is_active == 0:
        staff.is_active = 1
    else:
        staff.is_active = 0
    staff.save()
    return redirect('director_manage_staff')


@login_required()
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
        
        zt_obj.open_time = open
        zt_obj.close_time = close
        zt_obj.holiday = False
        zt_obj.save()
        return redirect("director_manage_zoo_time")

    else:
        return render(request,'view zoo time.html',{'time':zoo_time,'timeform':timeForm})


@login_required()
def markHoliday(request,id):
    zoo_time = ZooTimings.objects.get(pk=id)
    zoo_time.holiday = True
    zoo_time.save()
    return redirect('director_manage_zoo_time')


@login_required()
def visitorList(request):
    visitors = Users.objects.filter(usertype="visitor")
    return render(request,"visitor list.html",{'visitors':visitors})


@login_required()
def manageTicketRates(request):
    rateForm = TicketRateForm()
    rates = TicketRate.objects.all()

    if request.method == 'GET':
        return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})

    elif request.method == 'POST':
        form = TicketRateForm(request.POST)
        # ttype = request.POST.get('type')
        if form.is_valid():
            # print(form.data['type'],form.data['rate'])
            TicketRateHistory.objects.create(catagory = form.data['type'], rate = form.data['rate'])
            form.save()
            messages.success(request,"Ticket catagory added successfully")
            return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})
        else:
            messages.error(request,"error while submitting form")
            return render(request,"manageticketrates.html",{'form':form,'rates':rates,'error':True})
    else:
        return render(request,'manageticketrates.html',{'form':rateForm,'rates':rates})


@login_required()
def deleteTicketCatagory(request,id):
    catagory = TicketRate.objects.get(pk=id)
    catagory.delete()
    return redirect('director_manage_ticket_rate')


@login_required()
def UpdateTicketRate(request,id):
    rateObj = TicketRate.objects.get(pk=id)
    ticketRate = request.POST['rate']
    rates = TicketRate.objects.all()

    if int(ticketRate) < 0:
        messages.error(request,'Please provide a valid rate')
        return render(request,"manageticketrates.html",{'rates':rates,'update_error':True,'id':id})

    elif rateObj.rate == int(ticketRate):
        messages.error(request,'Data not saved, Please provide new ticket rate !')
        return render(request,"manageticketrates.html",{'rates':rates,'update_error':True,'id':id})

    else:
        TicketRateHistory.objects.create(catagory = rateObj.type, rate = rateObj.rate)
        rateObj.save()
        return redirect('director_manage_ticket_rate')


@login_required()
def viewTicketRateHistory(request):
    rateHistObj = TicketRateHistory.objects.all()
    return render(request,'view ticket rate history.html',{'ratehistory':rateHistObj})


@login_required()
def viewTicketSales(request):
    dic = {}
    catagories = []
    count = []
    tickets = Ticket.objects.values('tdate').annotate(tcount=Count('tdate')).order_by()
    id = Ticket.objects.values('id')

    for i in tickets:
        print(i['tdate'],i['tcount'])

    print(tickets)
    print(id)
    # print(tickets.values('tdate')[1]['tdate'])
    # print(tickets.values('tdate'))
    # print(tickets.values('tcount')[:].values('tcount'))

    # for i in tickets.values('tdate','id'):
    #     # print(i['tdate'])
    #     for j in BookedCatagory.objects.all():
    #         # print(j.ticket.id , i['id'])
    #         if j.ticket.id == i['id']:
    #             catagories.append(j.catagory)
    #     dic.update({i['tdate']:{'catagories':catagories}})
    
    # print(dic)

    # obj = BookedCatagory.objects.values('ticket').annotate(tcount=Count('ticket')).order_by()
    # print(obj)

    
    
    catagory = BookedCatagory.objects.all()
    return render(request,'view ticket sales.html',{'tickets':tickets,'catagory':catagory,'id':id})


@login_required()
def vacancyList(request):
    vacancy = JobVacancy.objects.all()
    return render(request,'manage vacancy.html',{'vacancies':vacancy})


@login_required()
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


@login_required()
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

@login_required()
def closeVacancy(request,id):
    catagory = JobVacancy.objects.get(pk=id)
    vacancy = JobVacancy.objects.all()
    catagory.vstatus = "closed"
    catagory.save()
    return render(request,'manage vacancy.html',{'message':True,'vacancies':vacancy})


@login_required()
def eventsList(request):
    events = Events.objects.all()
    current_date = date.today()

    for event in events:
        if event.estart > current_date:
            event.estatus = "upcoming"
        elif event.estart <= current_date <= event.eend:
            event.estatus = "ongoing"
        else:
            event.estatus = "finished"
        event.save()
    
    return render(request,'manage events.html',{'events':events})


@login_required()
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


@login_required()
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


@login_required()
def animalList(request):
    animals = Animals.objects.all()
    available = Animals.objects.filter(status=1)
    dead = Animals.objects.exclude(death_date = None)
    return render(request,'view animal.html',{'animals':animals,'available':available,'dead':dead})


@login_required()
def showAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    return render(request,'viewanimaldetails.html',{'animal':animal})


@login_required()
def enclosureList(request):
    enclosures = Enclosures.objects.all()
    return render(request,"enclosures list.html",{'enclosures':enclosures})


@login_required()
def showPurchases(request):
    purchase = Purchase.objects.all()
    return render(request,'view purchase history.html',{'purchase':purchase})


@login_required()
def viewTransferDetails(request):
    transferDetails = TransferDetails.objects.all()
    return render(request,'director view transfer details.html',{'transfers':transferDetails})


@login_required()
def sponserList(request):
    sponsers = SponserDetails.objects.all()
    return render(request,"manage sponsers.html",{'sponsers':sponsers})


@login_required()
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
            if SponserDetails.objects.filter(name=request.POST['name'],address=request.POST['address'],phone=request.POST['phone'],email=request.POST['email'],stype=request.POST['stype']).exists():
                sponserObj = SponserDetails.objects.get(name=request.POST['name'],address=request.POST['address'],phone=request.POST['phone'],email=request.POST['email'],stype=request.POST['stype'])
            else: 
                form1.save()
                sponserObj = SponserDetails.objects.get(name=request.POST['name'],address=request.POST['address'],phone=request.POST['phone'],email=request.POST['email'],stype=request.POST['stype'])
                
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


@login_required()
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


@login_required()
def showSponseredAnimals(request,id):
    animals = SponseredAnimals.objects.filter(sponser = id)
    return render(request,'sponsered animal details.html',{'animals':animals})


@login_required()
def deleteSponseredAnimal(request,id):
    animal = SponseredAnimals.objects.get(pk = id)
    animal.delete()
    messages.success(request,"sponsered animal deleted successfully!")
    return redirect('director_manage_sponsers')


@login_required()
def deleteSponser(request,id):
    sponser = SponserDetails.objects.get(pk=id)
    sponser.delete()
    return redirect('director_manage_sponsers')


@login_required()
def showFeedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request,'director view feedbacks.html',{'feedbacks':feedbacks})


@login_required()
def viewComplaints(request):
    complaints = Complaints.objects.filter(rid = Staffs.objects.get(user=request.user.id))

    if request.method == 'GET':
        return render(request,'director view complaints.html',{'complaints':complaints})
    
    elif request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        reply = request.POST.get('reply')
        
        complaint_obj = Complaints.objects.get(pk=complaint_id)
        complaint_obj.reply = reply
        complaint_obj.save()
        return redirect('director_view_complaints')

    else:
        return render(request,'director view complaints.html',{'complaints':complaints})


@login_required()
def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)

    if request.method == 'GET':
        return render(request,'director update profile.html',{'form':profileForm,'imageform':profileImageForm})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('director_view_profile')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'director update profile.html',{'form':form})

    else:
        return render(request,'director update profile.html',{'form':profileForm})


@login_required()
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


@login_required()
def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('director_view_profile')


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
            return redirect('director_view_profile')
    else:
        messages.error(request,'current password is wrong!')
        return redirect('director_view_profile')


@login_required()
def viewReport(request):
    
    if request.method == 'GET':
        return render(request,'view report.html')

    elif request.method == 'POST':
        from_date = request.POST['from']
        to_date = request.POST['to']

        if to_date.__le__(str(date.today())) == True:

            try:

                context = {
                    'report':True,
                    'visitors':Users.objects.filter(date_joined__range = [from_date,to_date],usertype = 'visitor').count(),
                    'total_visitors':Users.objects.filter(usertype = 'visitor').count(),
                    'total_staffs':Users.objects.filter(Q(usertype = 'curator') | Q(usertype = 'doctor') | Q(usertype = 'keeper')).count(),
                    'staffs':Users.objects.filter(date_joined__range = [from_date,to_date],usertype = ['curator','doctor','keeper']).count(),
                    'ticket':Ticket.objects.filter(tdate__range = [from_date,to_date]).count(),
                    'ticket_revenue':sum(Ticket.objects.filter(tdate__range = [from_date,to_date]).values_list('total',flat=True)),
                    'enclosure_count':Enclosures.objects.all().count(),
                    'enclosure_name':Enclosures.objects.all().values_list('name',flat=True),
                    'archived_count':Enclosures.objects.filter(archieved = True).count(),
                    'archived':Enclosures.objects.filter(archieved = True),
                    'animals':Animals.objects.filter(date_joined__range = [from_date,to_date], status =1).count(),
                    'total_animals':Animals.objects.filter(status = 1).count(),
                    'transfer_from':TransferDetails.objects.filter(transfer_date__range = [from_date,to_date],transfer_from = ZooDetails.objects.all().values_list('name',flat=True)[0]).count(),
                    'transfer_to':TransferDetails.objects.filter(transfer_date__range = [from_date,to_date],transfer_to = ZooDetails.objects.all().values_list('name',flat=True)[0]).count(),
                    'transfer_expenditure':sum(TransferDetails.objects.filter(transfer_date__range = [from_date,to_date]).values_list('expense',flat=True)),
                    'total_medicines':Medicines.objects.all().count(),
                    'stock_medicines':Medicines.objects.exclude(stock = 0).count(),
                    'out_of_stock_nedicines':Medicines.objects.filter(stock = 0).count(),
                    'sickness_count':sickness_details.objects.filter(sdate__range = [from_date,to_date]).count(),
                    'cured':sickness_details.objects.filter(sdate__range = [from_date,to_date], status = 'cured').count(),
                    'sick':sickness_details.objects.filter(sdate__range = [from_date,to_date], status = 'sick').count(),
                    'purchase':Purchase.objects.filter(pdate__range = [from_date,to_date]).count(),
                    'purchase_expenditure':sum(Purchase.objects.filter(pdate__range = [from_date,to_date]).values_list('price',flat=True)),
                    'events':Events.objects.filter(estart__range = [from_date,to_date]).count(),
                    'event_names':Events.objects.filter(estart__range = [from_date,to_date]).values_list('ename',flat=True),
                    'vacancy':JobVacancy.objects.filter(Q(vstart__gte = from_date) | Q(vend__gte = to_date)).count(),
                    'application_recieved':Applications.objects.filter(date__range = [from_date,to_date]).count(),
                    'application_accepted':Applications.objects.filter(date__range = [from_date,to_date],status = 'accepted').count(),
                    'application_rejected':Applications.objects.filter(date__range = [from_date,to_date],status = 'rejected').count(),
                    'feedback':Feedback.objects.filter(fdate__range = [from_date,to_date]).count(),
                    'feedback_replied':Feedback.objects.filter(fdate__range = [from_date,to_date]).exclude(reply = 'NULL').count(),
                    'complaint':Complaints.objects.filter(cdate__range = [from_date,to_date]).count(),
                    'complaint_replied':Complaints.objects.filter(cdate__range = [from_date,to_date]).exclude(reply = 'NULL').count(),
                    'sponser':SponserDetails.objects.filter(joined_date__range = [from_date,to_date]).count(),
                    'sponsered_animals':SponseredAnimals.objects.filter(Q(sdate__gte = from_date) | Q(edate__gte = to_date)).count(),
                    'sponser_revenue':sum(SponseredAnimals.objects.filter(Q(sdate__gte = from_date) | Q(edate__lte = to_date)).values_list('amount',flat=True)),
                }

                context['total_revenue'] = context['ticket_revenue'] + context['sponser_revenue']
                context['total_expense'] = context['transfer_expenditure'] + context['purchase_expenditure']
                
                context['from'] = from_date
                context['to'] = to_date
                

            except Exception as e:
                pass

            return render(request,'view report.html',context)

        else:
            messages.error(request,'to date is greater than current date, Report generation failed !')
            return render(request,'view report.html')

    else:
        return render(request,'view report.html')
