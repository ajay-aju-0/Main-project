from django.urls import path
from .views import *


urlpatterns = [
   path('home/',loadDirectorHome,name='director_home'),
]