from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from .forms import *
from datetime import date
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