from django.urls import path
from .views import *


urlpatterns = [
    path('home/',loadVisitorHome,name='visitor_home'),
]