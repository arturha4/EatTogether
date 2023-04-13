from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.cooperation, name='events'),
    path('create-event/', views.cooperation, name='create-event'),
    path('event-detail/<int:event_id>/', views.event_detail, name='event-detail'),
    path('join-event/<int:event_id>/', views.join_event, name='join_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('leave_event/<int:event_id>/', views.leave_event, name='leave_event'),
    path('delete_participant/<int:participant_id>/', views.delete_participant, name='delete_participant')
]

