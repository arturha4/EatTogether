from django.urls import path
from . import views


urlpatterns = [
    path('add-food/', views.add_food_to_fridge, name='add-food'),
    path('my/', views.FridgeIngredientView.as_view()),
    # path('recomendations/', views.recommended_food, name='recommended-food')
]