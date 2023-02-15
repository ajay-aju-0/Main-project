from django.shortcuts import render

# Create your views here.

def loadDirectorHome(request):
    return render(request,'directorHome.html')