from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from .forms import *
from datetime import date
from Director.forms import *
from django.contrib.auth import authenticate
from django.contrib import messages
# Create your views here.

def loadVisitorHome(request):
    return render(request,'visitorhome.html')

def viewTickets(request):
    tickets = Ticket.objects.filter(uid = request.user.id)
    Ticket.objects.filter(payment_status=False).delete()
    current_date = date.today()
    return render(request,'view tickets.html',{'tickets':tickets,'current':current_date})

def showTicketDetails(request,id):
    catagories = BookedCatagory.objects.filter(ticket = id)
    return render(request,'ticket details.html',{'catagories':catagories})

def bookTicket(request):
    ticketform = TicketForm()
    catagories = TicketRate.objects.all()
    if request.method == 'GET':
        return render(request,'book ticket.html',{'form':ticketform,'catagories':catagories})

    elif request.method == 'POST':
        form = TicketForm(request.POST)
        tRate =TicketRate.objects.all()

        if form.is_valid():
            obj = form.save(commit=False)
            count_list = request.POST.getlist('catagory')
            i = 0
            total = 0
            total_count = 0
            for rate in tRate:

                if int(count_list[i]) != 0:
                    catagory_rate = TicketRate.objects.get(type=rate.type)
                    total += int(count_list[i]) * catagory_rate.rate
                    total_count += int(count_list[i]) 

                i = i+1

            obj.total = total
            obj.total_person = total_count
            obj.uid = request.user
            obj.save()

            j=0
            for rate in tRate:
                if int(count_list[j]) != 0:
                    BookedCatagory.objects.create(catagory = TicketRate.objects.get(type=rate.type).type,count = count_list[j],rate = TicketRate.objects.get(type=rate.type).rate,ticket = obj)
                j=j+1
            
            return redirect('visitor_confirm_booking')
        else:
            return render(request,'book ticket.html',{'form':form,'catagories':catagories})
    else:
        return render(request,'book ticket.html',{'form':ticketform,'catagories':catagories})    


def confirmBooking(request):
    ticketStatus = Ticket.objects.filter(payment_status = False).exists()
    if ticketStatus:
        obj = Ticket.objects.get(payment_status=False)
    return render(request,'confirm booking.html',{'ticket':obj})

def declinePayment(request,id):
    ticket = Ticket.objects.get(pk=id)
    ticket.delete()
    return redirect('visitor_view_tickets')

def acceptPayment(request,id):
    ticket = Ticket.objects.get(pk=id)
    ticket.payment_status = True
    ticket.save()
    return redirect('visitor_view_tickets')


def cancelBooking(request,id):
    ticket = Ticket.objects.get(pk=id)
    ticket.delete()
    return redirect('visitor_view_tickets')


def showFeedbacks(request):
    feedbacks = Feedback.objects.filter(uid = request.user.id)
    feedbackForm = FeedbackForm()

    if request.method == 'GET':
        return render(request,'visitor view feedbacks.html',{'feedbacks':feedbacks,'form':feedbackForm})

    elif request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = request.user
            obj.save()
            return redirect('visitor_view_feedback')
        else:
            return render(request,"visitor view feedbacks.html",{'feedbacks':feedbacks,'form':form,'error':True})
    else:
        return render(request,'visitor view feedbacks.html',{'feedbacks':feedbacks,'form':feedbackForm})


def deleteFeedback(request,id):
    feedback = Feedback.objects.get(pk=id)
    feedback.delete()
    return redirect('visitor_view_feedback')

def viewComplaints(request):
    complaints = Complaints.objects.filter(uid = request.user.id)
    recipient = Users.objects.filter(usertype__in = ['curator','director'])
    # print(recipient[0].usertype)
    complaintForm = ComplaintForm()

    if request.method == 'GET':
        return render(request,'visitor view complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})

    elif request.method == 'POST':
        recipient = request.POST['recipient']
        form = ComplaintForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.uid = Users.objects.get(pk=request.user.id)
            obj.rid = Staffs.objects.get(user=recipient)
            obj.save()
            return redirect('visitor_view_complaints')
        else:
            return render(request,"visitor view complaints.html",{'complaints':complaints,'form':form,'recipients':recipient,'error':True})
    else:
        return render(request,'visitor view complaints.html',{'complaints':complaints,'form':complaintForm,'recipients':recipient})

def deleteComplaint(request,id):
    complaint = Complaints.objects.get(pk=id)
    complaint.delete()
    return redirect('visitor_view_complaints')

def viewProfile(request):
    profileForm = UpdateProfileForm(instance=request.user)
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'GET':
        return render(request,'visitor update profile.html',{'form':profileForm,'imageform':profileImageForm})

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('visitor_view_profile')
        else:
            messages.error(request,'Error while submitting form')
            return render(request,'visitor update profile.html',{'form':form})
    else:
        return render(request,'visitor update profile.html',{'form':profileForm})

def updateProfileImage(request):
    profileImageForm = ProfileImageForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST,request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'profile image updated successfully')
            return redirect('visitor_view_profile')
        else:
            return render(request,'visitor update profile.html',{'form':form,'imageform':profileImageForm,'error':True})

def deleteProfileImage(request):
    userObj = Users.objects.get(pk=request.user.id)
    userObj.profile = 'null'
    userObj.save()
    messages.success(request,'profile photo deleted successfully!')
    return redirect('visitor_view_profile')

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
            return redirect('visitor_view_profile')
    else:
        messages.error(request,'current password is wrong!')
        return redirect('visitor_view_profile')

def viewVacancy(request):
    vacancy = JobVacancy.objects.all()
    application = Applications.objects.filter(uid = request.user.id)
    return render(request,'view vacancy.html',{'vacancies':vacancy,'appl_obj':application})

def apply(request,id):
    vacancy = JobVacancy.objects.get(pk=id)
    applicationForm = ApplicationForm()

    if request.method == 'GET':
        return render(request,'apply job.html',{'form':applicationForm,'vacancy':vacancy})

    elif request.method == 'POST':
        form = ApplicationForm(request.POST,request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.vacancy = vacancy
            obj.uid = request.user
            obj.status = 'unreviewed'
            obj.save()
            messages.success(request,'Application submitted successfully!')
            return redirect('visitor_view_vacancy')
        else:
            messages.error(request,'Error while submitting form!')
            return render(request,'apply job.html',{'form':form,'vacancy':vacancy})
    else:
        return render(request,'apply job.html',{'form':applicationForm,'vacancy':vacancy})

def viewApplications(request):
    applications = Applications.objects.filter(uid = request.user.id)
    return render(request,'view applications.html',{'applications':applications})

def deleteApplication(request,id):
    application = Applications.objects.get(pk=id)
    application.delete()
    return redirect('visitor_view_job_application')