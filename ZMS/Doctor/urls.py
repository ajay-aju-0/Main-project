from django.urls import path
from Doctor.views import *


urlpatterns = [
   path('home/',loadDoctorHome,name="doctor_home"),
   path('verify animals/',animalVerification,name='doctor_verify_animals'),
   path('animal verified/<id>',verifyAnimal,name='doctor_verified_animal'),
   path('reject animal/',rejectAnimal,name='doctor_reject_reason'),
   path('animal health status/',viewAnimalHealth,name='doctor_view_health_status'),
   path('change animal health status/<id>',changeAnimalHealthStatus,name='curator_change_animal_health_status'),
   path('manage sick animals/',sickAnimalList,name='doctor_manage_sick_animals'),
   path('add sickness details/',addSickness,name='doctor_add_sickness_details'),
   path('manage medicines/',medicineList,name='doctor_manage_medicines'),
   path('update medicine/<id>',updateStock,name='doctor_update_medicine_stock'),
   path('delete medicine/<id>',deleteMedicine,name='doctor_delete_medicine'),
   path('mark cured/<id>',markCured,name='doctor_mark_animal_cured'),
   path('animal death details/',viewDeathDetails,name='doctor_manage_animal_death'),
   path('animal details/<id>',viewAnimalDetails,name='doctor_view_animal_details'),
   path('update death details/<id>',updateDeathDetails,name='doctor_update_death_details'),
   path('view complaint/',viewComplaints,name='doctor_view_complaints'),
   path('delete complaint/<id>',deleteComplaint,name='doctor_delete_complaint'),
   path('view profile/',viewProfile,name='doctor_view_profile'),
   path('upload profile image/',updateProfileImage,name='doctor_upload_profile_image'),
   path('delete profile/',deleteProfileImage,name='doctor_delete_profile_photo'),
   path('change password/',changePassword,name='doctor_change_password'),

   

]