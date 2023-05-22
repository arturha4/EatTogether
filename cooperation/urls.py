from django.urls import path
from . import views


urlpatterns = [
    path('', views.CooperationView.as_view(), name='cooperation'),
    path('<int:pk>/', views.CooperationDetail.as_view(), name='cooperation-detail')
]

