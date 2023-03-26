from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('home/', views.home),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout')
]