from django.urls import path
from .views import *


urlpatterns = [
    path('home/',loadKeeperHome,name='keeper_home'),
    path('animal health status/',viewAnimalHealthStatus,name='keeper_view_animal_health_status'),
    path('animal details/<id>',showAnimalDetails,name='keeper_view_animal_details'),
    path('health status/<id>',changeAnimalHealthStatus,name='keeper_change_animal_health_status'),
]