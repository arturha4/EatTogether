from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
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
    fridge_ingredients = FridgeIngredient.objects.filter(recip_ingredient_id=request.id)
    return render(request, 'fridge.html',
                  context={'user': request.user, 'ingredients': ingredients, 'fridge_ingredients': fridge_ingredients})


@login_required()
def add_food_to_fridge(request):
    if request.method == 'POST':
        data = request.POST

    return redirect('/my-fridge')
