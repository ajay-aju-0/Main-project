from django.urls import path
from .views import *


urlpatterns = [
    path('home/',loadVisitorHome,name='visitor_home'),
    path('view tickets/',viewTickets,name='visitor_view_tickets'),
    path('book ticket/',bookTicket,name='visitor_book_ticket'),
    path('confirm booking/',confirmBooking,name='visitor_confirm_booking'),
    path('decline payment/<id>',declinePayment,name='visitor_decline_payment'),
    path('accept payment/<id>',acceptPayment,name='visitor_accept_payment'),
    path('cancel ticket/<id>',cancelBooking,name='visitor_cancel_booking'),
    path('ticket details/<id>',showTicketDetails,name='visitor_view_ticket_details'),
    path('my feedback/',showFeedbacks,name='visitor_view_feedback'),
    path('delete feedback/<id>',deleteFeedback,name='visitor_delete_reply'),
    path('view complaints',viewComplaints,name='visitor_view_complaints'),
    path('delete complaint/<id>',deleteComplaint,name='visitor_delete_complaint')
]