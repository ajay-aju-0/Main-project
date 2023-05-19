from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from accounts.models import *
from .forms import *
from Director.forms import *
from Visitor.forms import *
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


@login_required()
def loadCuratorHome(request):
    staff_obj = Users.objects.exclude(Q(usertype = 'director') | Q(usertype ='visitor') | Q(usertype = 'curator')).filter(is_active = True).values('date_joined')
    visitor_obj = Users.objects.filter(usertype = 'visitor',is_active = True).values('date_joined')
    animal_obj = Animals.objects.filter(status = 1).values('date_joined')
    vacancy_obj = JobVacancy.objects.filter().values('issue_date')
    application_obj = Applications.objects.filter().values('date')
    ticket_obj = Ticket.objects.filter().values('tdate')
    purchase_obj = Purchase.objects.filter().values('pdate','price')

    visitors = []
    staffs = []
    animals = []
    vacancy = []
    application = []
    ticket = []
    purchase = []

    for i in visitor_obj:
        if i['date_joined'].year == date.today().year and i['date_joined'].month == date.today().month:
            visitors.append(i)

    for j in staff_obj:
        if j['date_joined'].year == date.today().year and j['date_joined'].month == date.today().month:
            staffs.append(j)

    for k in animal_obj:
        if k['date_joined'].year == date.today().year and k['date_joined'].month == date.today().month:
            animals.append(k)

    for l in vacancy_obj:
        if l['issue_date'].year == date.today().year and l['issue_date'].month == date.today().month:
            vacancy.append(l)

    for m in ticket_obj:
        if m['tdate'].year == date.today().year and m['tdate'].month == date.today().month:
            ticket.append(m)

    for n in application_obj:
        if n['date'].year == date.today().year and n['date'].month == date.today().month:
            application.append(n)

    for p in purchase_obj:
        if p['pdate'].year == date.today().year and p['pdate'].month == date.today().month:
            purchase.append(p['price'])

    context ={
        'visitors':len(visitors),
        'staffs':len(staffs),
        'animals':len(animals),
        'vacancy':len(vacancy),
        'application':len(application),
        'ticket':len(ticket),
        'purchase':sum(purchase),
    }

    return render(request,'curatorhome.html',context)


@login_required()
def viewEnclosures(request):
    enclosure = Enclosures.objects.all()
    enclosureForm = EnclosureForm()
    dismantleForm = DismantleEnclosureForm()
    
    if request.method == 'GET':
        return render(request,'view enclosures.html',{'enclosures':enclosure,'form':enclosureForm,'dismantleform':dismantleForm})

    elif request.method == 'POST':
        form = EnclosureForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.archieved = False
            obj.save()
            messages.success(request,"Enclosure added successfully")
            return render(request,'view enclosures.html',{'form':form,'enclosures':enclosure})
        else:
            return render(request,"view enclosures.html",{'form':form,'enclosures':enclosure,'error':True})


@login_required()
def changeEnclosureStatus(request,id):
    enclosure = Enclosures.objects.get(pk=id)
    if enclosure.archieved == 0:
        enclosure.archieved = 1
    else:
        enclosure.archieved = 0
    enclosure.save()
    messages.success(request,'Status changed sucessfully')
    return redirect('curator_manage_enclosures')


@login_required()
def dismantleEnclosure(request,id):
    enclosures = Enclosures.objects.all()
    enclosure = Enclosures.objects.get(pk=id)
    if request.method == 'POST':
        form = DismantleEnclosureForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.enclosure = enclosure
            obj.save()

            enclosure.delete()
            messages.success(request,'Enclosure dismantled sucessfully')
            return redirect('curator_manage_enclosures')
        else:
            messages.error(request,"error while submitting form")
            return render(request,"view enclosures.html",{'dismantleform':form,'enclosures':enclosures,'error':True})
    return redirect('curator_manage_enclosures')


@login_required()
def viewDismantledEnclosures(request):
    enclosures = DismantledEnclosures.objects.all()
    return render(request,'dismantled enclosures.html',{'enclosures':enclosures})


@login_required()
def viewAnimals(request):
    animals = Animals.objects.all()
    available = Animals.objects.filter(status=1)
    dead = Animals.objects.exclude(death_date = None)
    return render(request,'view animals.html',{'animals':animals,'available':available,'dead':dead})


@login_required()
def addAnimal(request):
    animalFormObj = AnimalForm()
    users = Users.objects.filter(usertype='keeper')
    animalKindFormObj = AnimalKindForm()
    taxonomyForm = TaxonomyForm()

    if request.method == 'GET':
        return render(request,'add animal.html',{'form1':animalFormObj,'keepers':users,'form2':animalKindFormObj,'form3':taxonomyForm})

    elif request.method == 'POST':
        enclosureobj = request.POST['location']
        enclosure = Enclosures.objects.get(id = enclosureobj)
        caretakerobj = request.POST['caretaker']
        
        
        form1 = AnimalForm(request.POST,request.FILES)
        form2 = AnimalKindForm(request.POST)
        form3 = TaxonomyForm(request.POST)

        if form1.is_valid() and form2.is_valid() and form3.is_valid():

            if caretakerobj != 'none':

                caretaker = Staffs.objects.get(user=caretakerobj)

                obj1 = form1.save(commit=False)
                obj1.location = enclosure
                obj1.caretaker = caretaker
                obj1.status = -1

                AclassCheck = Taxonomy.objects.filter(Aclass = request.POST['Aclass']).exists()
                AkindCheck = AnimalKind.objects.filter(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder']).exists()
                # print(AclassCheck,AkindCheck)

                if AclassCheck:
                    obj2 = Taxonomy.objects.get(Aclass = request.POST['Aclass'])
                    if AkindCheck:
                        obj3 = AnimalKind.objects.get(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'])
                        obj1.akind = obj3
                        obj2.save()
                        obj3.save()
                        obj1.save()
                    else:
                        obj3 = form2.save(commit=False)
                        obj3.class_id = obj2
                        obj1.akind = obj3
                        obj2.save()
                        obj3.save()
                        obj1.save()
                else:
                    obj2 = form3.save(commit=False)
                    if AkindCheck:
                        obj3 = AnimalKind.objects.get(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'])
                        obj1.akind = obj3
                        obj2.save()
                        obj3.save()
                        obj1.save()
                    else:
                        obj3 = form2.save(commit=False)
                        obj3.class_id = obj2
                        obj1.akind = obj3
                        obj2.save()
                        obj3.save()
                        obj1.save()
                messages.success(request,"Animal added successfully")
                return redirect('curator_manage_animals')
            else:
                messages.error(request,'Please mention the caretaker of the animal')
                return render(request,'add animal.html',{'form1':form1,'keepers':users,'form2':form2,'form3':form3})
        else:
            messages.error(request,"error while updating")
            return render(request,'add animal.html',{'form1':form1,'keepers':users,'form2':form2,'form3':form3})
    else:
        return render(request,'add animal.html',{'form1':animalFormObj,'keepers':users,'form2':animalKindFormObj,'form3':taxonomyForm})


@login_required()
def updateAnimal(request,id):
    animal = Animals.objects.get(pk=id)
    animalKind = AnimalKind.objects.get(pk=animal.akind.id)
    taxonomy = Taxonomy.objects.get(pk=animalKind.class_id.id)
    users = Users.objects.filter(usertype='keeper')
    current_ct = Users.objects.get(id=animal.caretaker.id)

    if request.method == 'GET':
        animalForm = UpdateAnimalForm(instance=animal)
        animalKindForm = AnimalKindForm(instance=animalKind)
        taxonomyForm = TaxonomyForm(instance=taxonomy)
        return render(request,'update animal.html',{'form1':animalForm,'form2':animalKindForm,'form3':taxonomyForm,'keepers':users,'current':current_ct})

    elif request.method == 'POST':
        form1 = UpdateAnimalForm(request.POST,instance=animal)
        form2 = AnimalKindForm(request.POST,instance=animalKind)
        form3 = TaxonomyForm(request.POST,instance=taxonomy)
        
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            AclassCheck = Taxonomy.objects.filter(Aclass = request.POST['Aclass']).exists()
            AkindCheck = AnimalKind.objects.filter(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder']).exists()
            
            if AclassCheck:
                if AkindCheck:
                    obj1 = form1.save(commit=False)
                    obj1.akind = AnimalKind.objects.get(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'])
                    obj1.status = -1
                    obj1.save()
                else:
                    AnimalKind.objects.create(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'],avg_lifespan = request.POST['avg_lifespan'],habitat = request.POST['habitat'],origin = request.POST['origin'],characteristics = request.POST['characteristics'],class_id =Taxonomy.objects.get(Aclass = request.POST['Aclass']))
                    obj2 = AnimalKind.objects.get(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'],avg_lifespan = request.POST['avg_lifespan'],habitat = request.POST['habitat'],origin = request.POST['origin'],characteristics = request.POST['characteristics'],class_id =Taxonomy.objects.get(Aclass = request.POST['Aclass']).id)
                    obj1 = form1.save(commit=False)
                    obj1.akind = obj2
                    obj1.status = -1
                    obj1.save()
            else:
                Taxonomy.objects.create(Aclass = request.POST['Aclass'])
                AnimalKind.objects.create(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'],avg_lifespan = request.POST['avg_lifespan'],habitat = request.POST['habitat'],origin = request.POST['origin'],characteristics = request.POST['characteristics'],class_id =Taxonomy.objects.get(Aclass = request.POST['Aclass']).id)
                obj2 = AnimalKind.objects.get(general_name = request.POST['general_name'],species = request.POST['species'],Aorder = request.POST['Aorder'],avg_lifespan = request.POST['avg_lifespan'],habitat = request.POST['habitat'],origin = request.POST['origin'],characteristics = request.POST['characteristics'],class_id =Taxonomy.objects.get(Aclass = request.POST['Aclass']).id)
                obj1 = form1.save(commit=False)
                obj1.akind = obj2
                obj1.status = -1
                obj1.save()
            messages.success(request,'Animal updated successfully')
            return redirect('curator_manage_animals')
        else:
            messages.error(request,"error while updating")
            return render(request,'add animal.html',{'form1':form1,'keepers':users,'form2':form2,'form3':form3})
    else:
        return redirect('curator_manage_animals')


@login_required()
def viewAnimalOfWeek(request):
    form = AnimalOfTheWeekForm()
    if request.method == 'GET':
        animalOfWeek = Animal_of_the_week.objects.all()
        return render(request,'view animal of the week.html',{'AOW':animalOfWeek,'form':form})

    elif request.method == 'POST':
        form = AnimalOfTheWeekForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Performance uploaded successfully")
            return redirect('curator_view_animal_of_the_week')
        else:
            return render(request,"view animal of the week.html",{'form':form,'error':True})
    else:
        return render(request,'view animal of the week.html',{'AOW':animalOfWeek,'form':form})


@login_required()
def deletePerformance(request,id):
    obj = Animal_of_the_week.objects.get(pk=id)
    obj.delete()
    messages.success(request,'Performance deleted successfully')
    return redirect('curator_view_animal_of_the_week')


@login_required()
def viewTransferDetails(request):
    form = TransferDetailsForm()
    if request.method == 'GET':
        transferDetails = TransferDetails.objects.all()
        return render(request,'view transfer details.html',{'transfers':transferDetails,'form':form})

    elif request.method == 'POST':
        form = TransferDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Tranfer added successfully")
            return redirect('curator_view_transfer_details')
        else:
            return render(request,"view transfer details.html",{'form':form,'error':True})
    else:
        return render(request,'view transfer details.html',{'transfers':transferDetails,'form':form})


@login_required()
def viewPurchases(request):
    purchases = Purchase.objects.all()
    purchaseForm = PurchaseForm()
    if request.method == 'GET':
        return render(request,'view purchases.html',{'purchases':purchases,'form':purchaseForm})

    elif request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Purchase data added successfully")
            return redirect('curator_manage_purchases')
        else:
            return render(request,"view purchases.html",{'form':form,'error':True})
    else:
        return render(request,'view purchases.html',{'purchases':purchases,'form':purchaseForm})


@login_required()
def deletePurchase(request,id):
    obj = Purchase.objects.get(pk=id)
    obj.delete()
    messages.success(request,'Purchase data deleted successfully')
    return redirect('curator_manage_purchases')


@login_required()
def staffList(request):
    staff = Staffs.objects.exclude(Q(desig = 'curator') | Q(desig = 'director'))
    return render(request,'stafflist.html',{'staffs':staff})


@login_required()
def addStaffs(request):
    regForm = StaffRegistrationForm()
    staffForm = StaffForm()
    if request.method == 'GET':
        return render(request,'add staff.html',{'form1':regForm,'form2':staffForm})
    elif request.method == 'POST':
        form1 = StaffRegistrationForm(request.POST,request.FILES)
        form2 = StaffForm(request.POST)
        passw = request.POST['password']
        if form1.is_valid() and form2.is_valid():
            obj1 = form1.save(commit=False)
            obj2 = form2.save(commit=False)
            obj1.set_password(passw)
            obj1.usertype = request.POST['desig']
            obj2.user = obj1
            obj1.save()
            obj2.save()
            messages.success(request,"Staff registered successfully")
            return redirect('curator_manage_staffs')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'add staff.html',{'form1':form1,'form2':form2})
    else:
        return render(request,'add staff.html',{'form1':regForm,'form2':staffForm})


@login_required()
def updateStaffs(request,id):
    staff = Staffs.objects.get(user=id)
    uname = Users.objects.get(pk=id)
    if request.method == 'GET':
        context = {}
        context['form'] = StaffForm(instance=staff)
        context['uname'] = uname
        return render(request, 'curatorupdatestaff.html', context)
    
    elif request.method == 'POST':
        form = StaffForm(request.POST,instance=staff)
        utype = request.POST['desig']
        if form.is_valid():
            form.save()
            uname.usertype = utype
            uname.save()
            messages.success(request,"Staff Updated successfully")
            return redirect('curator_manage_staffs')
        else:
            messages.error(request,'error while submitting form')
            return render(request,'curatorupdatestaff.html',{'form':form,'staff':True})
    else:
        return redirect('curator_manage_staffs')


@login_required()
def curatorChangeStaffStatus(request,id):
    staff = Users.objects.get(pk=id)
    if staff.is_active == 0:
        staff.is_active = 1
    else:
        staff.is_active = 0
    staff.save()
    messages.success(request,'Staff staus changed successfully')
    return redirect('curator_manage_staffs')


@login_required()
def visitorList(request):
    visitors = Users.objects.filter(usertype='visitor')
    return render(request,'view visitors.html',{'visitors':visitors})


@login_required()
def changeVisitorStatus(request,id):
    visitor = Users.objects.get(pk=id)
    if visitor.is_active == 1:
        visitor.is_active = 0
    else:
        visitor.is_active = 1
    visitor.save()
    messages.success(request,'Visitor status changed successfully')
    return redirect('curator_manage_visitors')


@login_required()
def eventsList(request):
    events = Events.objects.all()
    participants = Participants.objects.all()
    animals = Animals.objects.all()
    current_date = date.today()
    for event in events:
        # print(event.estart,event.eend)
        if event.estart > current_date:
            event.estatus = "upcoming"
        elif event.estart <= current_date <= event.eend:
            event.estatus = "ongoing"
        else:
            event.estatus = "finished"
        event.save()
    
    return render(request,'curator manage events.html',{'events':events,'participants':participants,'animals':animals})


@login_required()
def addParticipants(request,id):
    animals = Animals.objects.all()
    event = Events.objects.get(pk=id)
    if Participants.objects.filter(event=event.id).exists():
        participant_animals = Participants.objects.filter(event=event.id)
    else:
        participant_animals = []

    if request.method == 'GET':
        return render(request,'add participants.html',{'animals':animals,'event':event,'participants':participant_animals})

    elif request.method == 'POST':
        participants = request.POST.getlist('participants')
        # print(participants)
        if participants != []:
            for p in participants:
                participant = Participants()
                participant.event = event
                animal = Animals.objects.get(pk=p)
                participant.animal = animal
                participant.save()
            messages.success(request,'Participants added successfully')
            return redirect('curator_manage_events')
        else:
            messages.error(request,'Please select any animal as participants')
            return render(request,'add participants.html',{'animals':animals,'event':event,'participants':participant_animals})

    else:
        messages.error(request,'Error when adding participants')
        return render(request,'add participants.html',{'animals':animals,'event':event})


@login_required()
def removeParticipants(request,id):
    event = Events.objects.get(pk=id)
    animals = Participants.objects.filter(event=event)
    if request.method == 'GET':
        return render(request,'remove participants.html',{'participants':animals,'event':event})
    elif request.method == 'POST':
        participants = request.POST.getlist('participants')
        # print(participants)
        if participants != []:
            for p in participants:
                # print(event,p)
                participant = Participants.objects.get(event=event.id,animal=p)
                participant.delete()
            messages.success(request,'Participants removed successfully')
            return redirect('curator_manage_events')
        else:
            messages.error(request,'Please select any animal to remove them from participants list')
            return render(request,'remove participants.html',{'participants':animals,'event':event})
            
    else:
        messages.success(request,'Error occured when removing participants')
        return render(request,'remove participants.html',{'participants':animals,'event':event})


@login_required()
def viewAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    return render(request,'animaldetails.html',{'animal':animal})


@login_required()
def changeAnimalStatus(request,id):
    animal = Animals.objects.get(pk=id)
    
    if animal.status == 1:
        animal.status = 0
    else:
        animal.status = 1
    animal.save()
    messages.success(request,'Animal status changed successfully')
    return redirect('curator_manage_animals')


@login_required()
def vacancyList(request):
    vacancy = JobVacancy.objects.all()
    unreviewed_applications = Applications.objects.filter(status = 'unreviewed')
    return render(request,'curator view vacancy.html',{'vacancies':vacancy,'unreviewed':unreviewed_applications})


@login_required()
def viewApplications(request,id):
    applications = Applications.objects.filter(vacancy = id)
    return render(request,'curator view applications.html',{'applications':applications})


@login_required()
def acceptApplication(request,id,vid):
    vacancy = JobVacancy.objects.get(id = vid)
    application = Applications.objects.get(pk=id)
    application.status = 'accepted'
    application.save()
    messages.success(request,'Appication accepted successfully')
    return redirect('curator_view_applications',vacancy.id)


@login_required()
def rejectApplication(request,id,vid):
    vacancy = JobVacancy.objects.get(id = vid)
    application = Applications.objects.get(pk=id)
    application.status = 'rejected'
    application.save()
    messages.success(request,'Application rejected successfully')
    return redirect('curator_view_applications',vacancy.id)


@login_required()
def viewMedicineStocks(request):
    medicines = Medicines.objects.all()
    return render(request,'view medicine stocks.html',{'medicines':medicines})


@login_required()
def viewBookings(request):
    tickets = Ticket.objects.all()
    keepers = Users.objects.filter(usertype='keeper', is_active=True)

    if request.method == 'GET':
        return render(request,'view bookings.html',{'tickets':tickets,'keepers':keepers})
    
    elif request.method == 'POST':
        guide = request.POST.get('assign_guide')
        if guide != 'None':
            ticket = Ticket.objects.get(pk=request.POST.get('ticket'))
            ticket.Guide = Staffs.objects.get(user=guide)
            ticket.save()
            messages.success(request,'Guide assigned successfully')
            return redirect('curator_view_bookings')
        else:
            messages.error(request,'Error when assigning guide')
            return render(request,"view bookings.html",{'tickets':tickets,'keepers':keepers,'error':True})

    else:
        return render(request,'view bookings.html',{'tickets':tickets,'keepers':keepers})


@login_required()
def showBookingDetails(request,id):
    catagories = BookedCatagory.objects.filter(ticket = id)
    return render(request,'booking details.html',{'catagories':catagories})
    

@login_required()
def curatorViewFeedbacks(request):
    feedbacks = Feedback.objects.all()

    if request.method == 'GET':
        return render(request,'view feedbacks.html',{'feedbacks':feedbacks})

    elif request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        reply = request.POST.get('reply')
        print(feedback_id,reply)

        feedback_obj = Feedback.objects.get(pk=feedback_id)
        feedback_obj.reply = reply
        feedback_obj.save()
        messages.success(request,'Feedback send successfully')
        return redirect('curator_view_feedbacks')
    else:
        return render(request,'view feedbacks.html',{'feedbacks':feedbacks})


@login_required()
def deleteFeedback(request,id):
    feedback = Feedback.objects.get(pk=id)
    feedback.delete()
    messages.success(request,'Feedback deleted successfully')
    return redirect('curator_view_feedbacks')


@login_required()
def viewComplaints(request):
    complaints = Complaints.objects.filter(rid = Users.objects.get(pk=request.user.id))

    if request.method == 'GET':
        return render(request,'curator view complaints.html',{'complaints':complaints})
    
    elif request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        reply = request.POST.get('reply')
        # print(complaint_id,reply)

        complaint_obj = Complaints.objects.get(pk=complaint_id)
        complaint_obj.reply = reply
        complaint_obj.save()
        messages.success(request,'Complaint registered successfully')
        return redirect('curator_view_complaints')
    else:
        return render(request,'curator view complaints.html',{'complaints':complaints})


@login_required()
def viewGivenComplaints(request):
    complaints = Complaints.objects.filter(uid = request.user.id)
    recipient = Users.objects.filter(usertype__in = ['director'])
    # print(recipient[0].usertype)
    complaintForm = ComplaintForm()

    if request.method == 'GET':
        return render(request,'curator view given complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})

    elif request.method == 'POST':
        recipient = request.POST['recipient']
        form = ComplaintForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = Users.objects.get(pk=request.user.id)
            obj.rid = Users.objects.get(pk=recipient.id)
            obj.save()
            messages.success(request,'Reply send successfully')
            return redirect('curator_view_send_complaint')
        else:
            return render(request,"curator view given complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True})
    else:
        return render(request,'curator view given complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})


@login_required()
def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    messages.success(request,'Complaint deleted successfully')
    return redirect('curator_view_send_complaint')


@login_required()
def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'GET':
        return render(request,'curator update profile.html',{'form':profileForm,'imageform':profileImageForm})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('curator_view_profile')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'curator update profile.html',{'form':form})
    else:
        return render(request,'curator update profile.html',{'form':profileForm})


@login_required()
def updateProfileImage(request):
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST,request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile image updated successfully')
            return redirect('curator_view_profile')
        else:
            return render(request,'curator update profile.html',{'form':form,'imageform':profileImageForm,'error':True})


@login_required()
def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('curator_view_profile')


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
            return redirect('curator_view_profile')
    else:
        messages.error(request,'current password is wrong!')
        return redirect('curator_view_profile')
        