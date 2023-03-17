from django.shortcuts import render

# Create your views here.

def loadVisitorHome(request):
    return render(request,'visitorhome.html')
