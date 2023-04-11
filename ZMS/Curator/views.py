from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from accounts.models import *
from .forms import *
from Director.forms import *
from Visitor.forms import *
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate

# Create your views here.


def loadCuratorHome(request):
    return render(request,'curatorhome.html')

def viewEnclosures(request):
    enclosure = Enclosures.objects.all()
    enclosureForm = EnclosureForm()
    
    if request.method == 'GET':
        return render(request,'view enclosures.html',{'enclosures':enclosure,'form':enclosureForm})

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

def changeEnclosureStatus(request,id):
    enclosure = Enclosures.objects.get(pk=id)
    if enclosure.archieved == 0:
        enclosure.archieved = 1
    else:
        enclosure.archieved = 0
    enclosure.save()
    return redirect('curator_manage_enclosures')

def deleteEnclosure(request,id):
    enclosure = Enclosures.objects.get(pk=id)
    enclosure.delete()
    return redirect('curator_manage_enclosures')

def viewAnimals(request):
    animals = Animals.objects.all()
    return render(request,'view animals.html',{'animals':animals})

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
                print(3)
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

            

def deletePerformance(request,id):
    obj = Animal_of_the_week.objects.get(pk=id)
    obj.delete()
    return redirect('curator_view_animal_of_the_week')


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

def deleteTransfer(request,id):
    obj = TransferDetails.objects.get(pk=id)
    obj.delete()
    return redirect('curator_view_transfer_details')

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

def deletePurchase(request,id):
    obj = Purchase.objects.get(pk=id)
    obj.delete()
    return redirect('curator_manage_purchases')

def staffList(request):
    staff = Staffs.objects.exclude(Q(desig = 'curator') | Q(desig = 'director'))
    return render(request,'stafflist.html',{'staffs':staff})

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

def curatorChangeStaffStatus(request,id):
    staff = Users.objects.get(pk=id)
    if staff.is_active == 0:
        staff.is_active = 1
    else:
        staff.is_active = 0
    staff.save()
    return redirect('curator_manage_staffs')

def visitorList(request):
    visitors = Users.objects.filter(usertype='visitor')
    return render(request,'view visitors.html',{'visitors':visitors})

def changeVisitorStatus(request,id):
    visitor = Users.objects.get(pk=id)
    if visitor.is_active == 1:
        visitor.is_active = 0
    else:
        visitor.is_active = 1
    visitor.save()
    return redirect('curator_manage_visitors')

def eventsList(request):
    events = Events.objects.all()
    participants = Participants.objects.all()
    animals = Animals.objects.all()
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
    
    return render(request,'curator manage events.html',{'events':events,'participants':participants,'animals':animals})

def addParticipants(request,id):
    animals = Animals.objects.all()
    event = Events.objects.get(pk=id)
    if request.method == 'GET':
        return render(request,'add participants.html',{'animals':animals,'event':event})
    elif request.method == 'POST':
        participants = request.POST.getlist('participants')
        print(participants)
        for p in participants:
            participant = Participants()
            participant.event = event
            animal = Animals.objects.get(pk=p)
            participant.animal = animal
            participant.save()
        return redirect('curator_manage_events')
    else:
        return render(request,'add participants.html',{'animals':animals,'event':event})



def removeParticipants(request,id):
    event = Events.objects.get(pk=id)
    animals = Participants.objects.filter(event=event)
    if request.method == 'GET':
        return render(request,'remove participants.html',{'participants':animals,'event':event})
    elif request.method == 'POST':
        participants = request.POST.getlist('participants')
        # print(participants)
        for p in participants:
            print(event,p)
            participant = Participants.objects.get(event=event.id,animal=p)
            participant.delete()
        return redirect('curator_manage_events')
    else:
        return render(request,'remove participants.html',{'participants':animals,'event':event})

def viewAnimalDetails(request,id):
    animal = Animals.objects.get(pk=id)
    return render(request,'animaldetails.html',{'animal':animal})

def changeAnimalStatus(request,id):
    animal = Animals.objects.get(pk=id)
    
    if animal.status == 1:
        animal.status = 0
    else:
        animal.status = 1
    animal.save()
    return redirect('curator_manage_animals')

def vacancyList(request):
    vacancy = JobVacancy.objects.all()
    unreviewed_applications = Applications.objects.filter(status = 'unreviewed')
    return render(request,'curator view vacancy.html',{'vacancies':vacancy,'unreviewed':unreviewed_applications})

def viewApplications(request,id):
    applications = Applications.objects.filter(vacancy = id)
    return render(request,'curator view applications.html',{'applications':applications})

def acceptApplication(request,id,vid):
    vacancy = JobVacancy.objects.get(id = vid)
    application = Applications.objects.get(pk=id)
    application.status = 'accepted'
    application.save()
    return redirect('curator_view_applications',vacancy.id)

def rejectApplication(request,id,vid):
    vacancy = JobVacancy.objects.get(id = vid)
    application = Applications.objects.get(pk=id)
    application.status = 'rejected'
    application.save()
    return redirect('curator_view_applications',vacancy.id)

def viewMedicineStocks(request):
    medicines = Medicines.objects.all()
    return render(request,'view medicine stocks.html',{'medicines':medicines})

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
            return redirect('curator_view_bookings')
        else:
            return render(request,"view bookings.html",{'tickets':tickets,'keepers':keepers,'error':True})

    else:
        return render(request,'view bookings.html',{'tickets':tickets,'keepers':keepers})


def showBookingDetails(request,id):
    catagories = BookedCatagory.objects.filter(ticket = id)
    return render(request,'booking details.html',{'catagories':catagories})
    

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
        return redirect('curator_view_feedbacks')
    else:
        return render(request,'view feedbacks.html',{'feedbacks':feedbacks})

def deleteFeedback(request,id):
    feedback = Feedback.objects.get(pk=id)
    feedback.delete()
    return redirect('curator_view_feedbacks')

def viewComplaints(request):
    complaints = Complaints.objects.filter(rid = Staffs.objects.get(user=request.user.id))

    if request.method == 'GET':
        return render(request,'curator view complaints.html',{'complaints':complaints})
    
    elif request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        reply = request.POST.get('reply')
        print(complaint_id,reply)

        complaint_obj = Complaints.objects.get(pk=complaint_id)
        complaint_obj.reply = reply
        complaint_obj.save()
        return redirect('curator_view_complaints')
    else:
        return render(request,'curator view complaints.html',{'complaints':complaints})


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
            obj.rid = Staffs.objects.get(user=recipient)
            obj.save()
            return redirect('curator_view_send_complaint')
        else:
            return render(request,"curator view given complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True})
    else:
        return render(request,'curator view given complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})

def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    return redirect('curator_view_send_complaint')


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

def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('curator_view_profile')

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
