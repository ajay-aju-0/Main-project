from django.urls import path
from .views import *


urlpatterns = [
    path("visitor_registration/",visitorRegistration,name="register_visitor"),
]