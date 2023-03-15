from django.urls import path
from Director.views import *


urlpatterns = [
   path('home/',loadDirectorHome,name="director_home"),
   path('manage_staff/',staffList,name="director_manage_staff"),
   path('add_curator/',addCurator,name="director_add_curator"),
   path('update staff/<id>',updateStaff,name="director_update_staff"),
   path('staff change status/<id>',changeStaffStatus,name="director_change_staffstatus"),
   path('manage ticket rates/',manageTicketRates,name="director_manage_ticket_rate"),
   path('delete ticket catagory/<id>',deleteTicketCatagory,name="director_delete_ticket_catagory"),
   path('update ticket catagory/<id>',UpdateTicketCatagory,name="director_update_ticket_rate"),
   path('vacancy details/',vacancyList,name="director_manage_vacancy"),
   path('add vacancy/',addVacancy,name="director_add_vacancy"),
   path('update vacancy/<id>',updateVacancy,name="director_update_vacancy"),
   path('close vacancy/<id>',closeVacancy,name="director_close_vacancy"),
   path('view visitors/',visitorList,name="director_view_visitors"),
   path('zoo time/',showZooTime,name="director_manage_zoo_time"),
   path('view events/',eventsList,name="director_manage_events"),
   path('add event/',addEvents,name="director_add_event"),
   path('update event/<id>',updateEvents,name="director_update_event"),
   path('manage sponsers/',sponserList,name="director_manage_sponsers"),
   path('add sponser/',addSponser,name="director_add_sponser"),
   path('view enclosures/',enclosureList,name='director_view_enclosures'),
   path('view purchases/',showPurchases,name='director_view_purchase_history'),
   path('view animals/',animalList,name="director_view_animals"),

]