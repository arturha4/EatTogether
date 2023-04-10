from django.contrib import admin
from fridges.models import FridgeIngredient,  RecipIngredient, Recip

admin.site.register(FridgeIngredient)
admin.site.register(Recip)
admin.site.register(RecipIngredient)
