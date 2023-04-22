from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import RecipIngredient, FridgeIngredient
from rest_framework.views import APIView

from .serializers import FridgeIngredientSerializer


class FridgeIngredientView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        food = FridgeIngredient.objects.filter(user_id=request.user.id)
        serializer = FridgeIngredientSerializer(food, many=True)
        return Response(serializer.data)


@login_required()
def fridge(request):
    ingredients = RecipIngredient.objects.all()
    fridge_ingredients = FridgeIngredient.objects.filter(user_id=request.user.id)
    return render(request, 'fridge.html',
                  context={'user': request.user, 'ingredients': ingredients, 'fridge_ingredients': fridge_ingredients})


@login_required()
def add_food_to_fridge(request):
    if request.method == 'POST':
        data = request.POST
        existing_item = FridgeIngredient.objects.filter(name=data.get('food_name')).first()
        if existing_item:
            existing_item.quantity += int(data.get('quantity'))
            existing_item.save()
        else:
            recip_ingredient = RecipIngredient.objects.get(name=data.get('food_name'))
            fridge_ingredient = FridgeIngredient.objects.create(name=data.get('food_name'), quantity=data.get('quantity'),
                                                            unit=data.get('unit'), user=request.user, recip_ingredient=recip_ingredient,
                                                            expiration_date=data.get('expiration_date'))
            fridge_ingredient.save()
    return redirect('/my-fridge')

