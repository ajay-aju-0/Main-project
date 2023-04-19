from django.urls import path
from .views import *


urlpatterns = [
    path('home/',loadKeeperHome,name='keeper_home'),
    path('animal health status/',viewAnimalHealthStatus,name='keeper_view_animal_health_status'),
    path('animal details/<id>',showAnimalDetails,name='keeper_view_animal_details'),
    path('health status/<id>',changeAnimalHealthStatus,name='keeper_change_animal_health_status'),
    path('sick animals/',viewSickAnimals,name='keeper_manage_sick_animals'),
    path('update consumption/<id>/<medicine>',updateConsumption,name='keeper_update_medicine_consumption'),
    path('medicine consumption details/<id>',viewMedicineConsumption,name='keeper_view_given_medicine'),
    path('guiding slots/',viewGuidingSlots,name='keeper_view_guiding_slots'),
    path('view complaint/',viewComplaints,name='keeper_view_complaint'),
    path('delete complaint/<id>',deleteComplaint,name='keeper_delete_complaint'),
    path('view profile/',viewProfile,name='keeper_view_profile'),
    path('upload profile image/',updateProfileImage,name='keeper_upload_profile_image'),
    path('delete profile/',deleteProfileImage,name='keeper_delete_profile_photo'),
    path('change password/',changePassword,name='keeper_change_password'),
]