from rest_framework import serializers
from .models import FridgeIngredient, RecipIngredient, Recip


class FridgeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeIngredient
        fields = ('id', 'name', 'expiration_date', 'recip_ingredient', 'user', 'quantity', 'unit')


class RecipIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipIngredient
        fields = ('name',)


class RecipSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField(many=True)
    class Meta:
        model = Recip
        fields = ('name', 'description', 'ingredients')
