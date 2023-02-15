from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages



# Create your views here.

def loadHome(request):
    return render(request,'index.html')

def visitorRegistration(request):
    form = VisitorRegistrationForm(initial={"usertype":"visitor"})
    if request.method == 'GET':
        return render(request,'visitor registration.html',{'form':form})
    elif request.method == 'POST':
        regForm = VisitorRegistrationForm(request.POST,request.FILES)
        pwd = request.POST['password']
        print(regForm.data)
        if regForm.is_valid():
            obj = regForm.save(commit=False)
            obj.set_password(pwd)
            obj.save()
            messages.success(request,"Visitor registered successfully")
            return render(request,'visitor registration.html',{'form':form})
        else:
            messages.error(request, 'Invalid form submission.')
            return render(request,'visitor registration.html',{'form':regForm})
    else:
        return render(request,'visitor registration.html',{'form':form})
