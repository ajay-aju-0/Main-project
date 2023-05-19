from django.urls import path
from Curator.views import *


urlpatterns = [
   path('home/',loadCuratorHome,name='curator_home'),
   path('manage enclosures/',viewEnclosures,name='curator_manage_enclosures'),
   path('enclosure status/<id>',changeEnclosureStatus,name='curator_change_enclosurestatus'),
   path('dismantle enclosure/<id>',dismantleEnclosure,name='curator_dismantle_enclosure'),
   path('dismantled enclosures/',viewDismantledEnclosures,name='curator_view_dismantled_enclosures'),
   path('manage animals/',viewAnimals,name='curator_manage_animals'),
   path('add animal/',addAnimal,name='curator_add_animal'),
   path('update animal/<id>',updateAnimal,name='curator_update_animal'),
   path('animal of the week/',viewAnimalOfWeek,name='curator_view_animal_of_the_week'),
   path('remove performance/<id>',deletePerformance,name='curator_remove_animal_performance'),
   path('transfer details/',viewTransferDetails,name='curator_view_transfer_details'),
   path('manage purchases/',viewPurchases,name='curator_manage_purchases'),
   path('deletenpurchase/<id>',deletePurchase,name='curator_delete_purchase'),
   path('manage staffs/',staffList,name='curator_manage_staffs'),
   path('add staff/',addStaffs,name='curator_add_staffs'),
   path('update staff/<id>',updateStaffs,name='curator_update_staffs'),
   path('change staff status/<id>',curatorChangeStaffStatus,name='curator_change_staff_status'),
   path('manage visitors/',visitorList,name='curator_manage_visitors'),
   path('change visitor status/<id>',changeVisitorStatus,name='curator_change_visitor_status'),
   path('manage events/',eventsList,name='curator_manage_events'),
   path('add participants/<id>',addParticipants,name='curator_add_participants'),
   path('remove participants/<id>',removeParticipants,name='curator_remove_participants'),
   path('animal details/<id>',viewAnimalDetails,name='curator_view_animal_details'),
   path('change animal status/<id>',changeAnimalStatus,name='curator_change_animal_status'),
   path('view vacancy/',vacancyList,name='curator_view_vacancy'),
   path('view applications/<id>',viewApplications,name='curator_view_applications'),
   path('accept application/<id><vid>',acceptApplication,name='curator_accept_application'),
   path('reject application/<id><vid>',rejectApplication,name='curator_reject_application'),
   path('medicine stocks/',viewMedicineStocks,name='curator_view_medicine_stock'),
   path('view bookings/',viewBookings,name='curator_view_bookings'),
   path('view booking details/<id>',showBookingDetails,name='curator_view_ticket_details'),
   path('view feedback/',curatorViewFeedbacks,name='curator_view_feedbacks'),
   path('delete feedback/<id>',deleteFeedback,name='curator_delete_feedbacks'),
   path('view complaints/',viewComplaints,name='curator_view_complaints'),
   path('view given complaint/',viewGivenComplaints,name='curator_view_send_complaint'),
   path('delete complaint/<id>',deleteComplaint,name='curator_delete_complaint'),
   path('view profile/',viewProfile,name='curator_view_profile'),
   path('upload profile image/',updateProfileImage,name='curator_upload_profile_image'),
   path('delete profile/',deleteProfileImage,name='curator_delete_profile_photo'),
   path('change password/',changePassword,name='curator_change_password'),
   



]