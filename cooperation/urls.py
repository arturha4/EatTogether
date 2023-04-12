from django.urls import path
from . import views


urlpatterns = [
    path('create-event/', views.cooperation, name='create-event'),
    path('join-event/', views.join_event),
    path('home/', views.cooperation, name='events'),
    path('event-detail/<int:event_id>/', views.event_detail, name='event-detail'),
    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event')
]