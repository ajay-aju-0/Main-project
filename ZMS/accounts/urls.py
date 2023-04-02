from django.urls import path
from .views import *


urlpatterns = [
    path("visitor_registration/",visitorRegistration,name="register_visitor"),
    path('login/',loginUser,name='login_user'),
    path('login user',authenticatedUser,name='login_authenticated_user'),
    path('logout/',logoutUser,name='logout')
]