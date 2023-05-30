from django.urls import path
from . import views
from .views import RecommendationsAPIView

urlpatterns = [
    path('add-food/', views.add_food_to_fridge, name='add-food'),
    path('my/', views.FridgeIngredientView.as_view(), name='food'),
    path('recomendations/', RecommendationsAPIView.as_view(), name='recommended-food'),
    path('decode-barcode/', views.  decode_barcode)
]