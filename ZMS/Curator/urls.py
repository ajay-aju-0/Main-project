from django.urls import path
from Curator.views import *


urlpatterns = [
   path('home/',loadCuratorHome,name='curator_home'),
   path('manage enclosures/',viewEnclosures,name='curator_manage_enclosures'),
   path('enclosure status/<id>',changeEnclosureStatus,name='curator_change_enclosurestatus'),
   path('delete enclosure/<id>',deleteEnclosure,name='curator_delete_enclosure'),
   path('manage animals/',viewAnimals,name='curator_manage_animals'),
   path('add animal/',addAnimal,name='curator_add_animal'),
   path('update animal/<id>',updateAnimal,name='curator_update_animal'),
   path('animal of the week/',viewAnimalOfWeek,name='curator_view_animal_of_the_week'),
   path('remove performance/<id>',deletePerformance,name='curator_remove_animal_performance'),
   path('transfer details/',viewTransferDetails,name='curator_view_transfer_details'),
   path('delete transfer/<id>',deleteTransfer,name='curator_remove_animal_transfer'),
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
   path('medicine stocks/',viewMedicineStocks,name='curator_view_medicine_stock'),
   path('view bookings/',viewBookings,name='curator_view_bookings'),
   path('view booking details/<id>',showBookingDetails,name='curator_view_ticket_details'),
   path('view feedback/',curatorViewFeedbacks,name='curator_view_feedbacks'),
   path('delete feedback/<id>',deleteFeedback,name='curator_delete_feedbacks'),
   path('view complaints/',viewComplaints,name='curator_view_complaints'),
   path('view given complaint/',viewGivenComplaints,name='curator_view_send_complaint'),
   path('delete complaint/<id>',deleteComplaint,name='curator_delete_complaint')
   



]