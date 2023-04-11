from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control



# Create your views here.

def loadHome(request):
    return render(request,'index.html')    


def visitorRegistration(request):
    form = RegistrationForm(initial={"usertype":"visitor"})
    if request.method == 'GET':
        return render(request,'visitor registration.html',{'form':form})
    elif request.method == 'POST':
        regForm = RegistrationForm(request.POST,request.FILES)
        pwd = request.POST['password']
        if regForm.is_valid():
            obj = regForm.save(commit=False)
            obj.set_password(pwd)
            obj.save()
            messages.success(request,"Visitor registered successfully")
            return render(request,'visitor registration.html',{'form':form})
        else:
            messages.error(request, 'error while submitting form.')
            return render(request,'visitor registration.html',{'form':regForm})
    else:
        return render(request,'visitor registration.html',{'form':form})


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password)
        
        if user != None:
            user_type = user.usertype
            login(request,user)
            if user_type == 'admin':
                return redirect('/admin/')
            elif user_type == 'director':
                return redirect('director_home')
            elif user_type == 'curator':
                return redirect('curator_home')
            elif user_type == 'keeper':
                return redirect('keeper_home')
            elif user_type == 'doctor':
                return redirect('doctor_home')
            elif user_type == 'visitor':
                return redirect('visitor_home')
            else:
                return HttpResponse('requested page unavailable')
        else:
            messages.error(request,'invalid username or password')
            return render(request,'index.html',{'error':True})
    else:
        return render(request,'index.html')


def authenticatedUser(request):
    user_type = request.user.usertype
    login(request,request.user)
    if user_type == 'admin':
        return redirect('/admin/')
    elif user_type == 'director':
        return redirect('director_home')
    elif user_type == 'curator':
        return redirect('curator_home')
    elif user_type == 'keeper':
        return redirect('keeper_home')
    elif user_type == 'doctor':
        return redirect('doctor_home')
    elif user_type == 'visitor':
        return redirect('visitor_home')
    else:
        return HttpResponse('requested page unavailable')
 

def logoutUser(request):
    logout(request)
    request.user = None
    return redirect('home')