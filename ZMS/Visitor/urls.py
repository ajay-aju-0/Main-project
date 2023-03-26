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
    path('delete complaint/<id>',deleteComplaint,name='visitor_delete_complaint'),
    path('view vacancy/',viewVacancy,name='visitor_view_vacancy'),
    path('apply job/<id>',apply,name='visitor_apply_job'),
    path('view applications',viewApplications,name='visitor_view_job_application'),
    path('delete application/<id>',deleteApplication,name='visitor_delete_application'),
    path('view profile/',viewProfile,name='visitor_view_profile'),
    path('upload profile image/',updateProfileImage,name='visitor_upload_profile_image'),
    path('delete profile/',deleteProfileImage,name='visitor_delete_profile_photo'),
    path('change password/',changePassword,name='visitor_change_password'),
]