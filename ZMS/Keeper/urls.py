from django.urls import path
from .views import *


urlpatterns = [
    path('home/',loadKeeperHome,name='keeper_home'),
    path('animal health status/',viewAnimalHealthStatus,name='keeper_view_animal_health_status'),
    path('animal details/<id>',showAnimalDetails,name='keeper_view_animal_details'),
    path('health status/<id>',changeAnimalHealthStatus,name='keeper_change_animal_health_status'),
    path('view complaint/',viewComplaints,name='keeper_view_complaint'),
    path('delete complaint/<id>',deleteComplaint,name='keeper_delete_complaint'),
    path('view profile/',viewProfile,name='keeper_view_profile'),
    path('upload profile image/',updateProfileImage,name='keeper_upload_profile_image'),
    path('delete profile/',deleteProfileImage,name='keeper_delete_profile_photo'),
    path('change password/',changePassword,name='keeper_change_password'),
]