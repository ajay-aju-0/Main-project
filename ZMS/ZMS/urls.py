"""ZMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from accounts.views import *
from django.conf.urls.static import static
from django.conf import settings

handler400 = 'accounts.views.error_400'
handler403 = 'accounts.views.error_403'
handler404 = 'accounts.views.error_404'
handler500 = 'accounts.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loadHome,name="home"),
    path('accounts/',include('accounts.urls')),
    path('director/',include('Director.urls')),
    path('curator/',include('Curator.urls')),
    path('doctor/',include('Doctor.urls')),
    path('keeper/',include('Keeper.urls')),
    path('visitor/',include('Visitor.urls'))
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
