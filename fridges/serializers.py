from rest_framework import serializers
from .models import FridgeIngredient


class FridgeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeIngredient
        fields = ('id', 'name', 'expiration_date', 'recip_ingredient', 'user', 'quantity', 'unit')


