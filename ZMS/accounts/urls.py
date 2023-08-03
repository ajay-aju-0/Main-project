from django.urls import path
from .views import *


urlpatterns = [
    path("visitor_registration/",visitorRegistration,name="register_visitor"),
    path('view animals/',viewAnimals,name='view_animals'),
    path('view events/',viewEvents,name='view_events'),
    path('view feedbacks/',viewFeedbacks,name='view_feedbacks'),
    path('view schedules/',viewTimings,name='view_schedules'),
    path('login/',loginUser,name='login_user'),
    path('login user',authenticatedUser,name='login_authenticated_user'),
    path('logout/',logoutUser,name='logout')
]