import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from .models import RecipIngredient, FridgeIngredient, Recip
from rest_framework.views import APIView

from .serializers import FridgeIngredientSerializer, RecipSerializer
from .services import get_barcode_from_image, get_food_title, get_recipe_suggestion


class FridgeIngredientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        food = FridgeIngredient.objects.filter(user_id=request.user.id)
        serializer = FridgeIngredientSerializer(food, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.POST
        try:
            existing_item = FridgeIngredient.objects.get(name=data.get('food_name'))
        except:
            existing_item = None
        if existing_item:
            existing_item.quantity += int(data.get('quantity'))
            existing_item.save()
            serializer = FridgeIngredientSerializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            recip_ingredient = RecipIngredient.objects.get(name=data.get('food_name'))
            fridge_ingredient = FridgeIngredient.objects.create(name=data.get('food_name'),
                                                                quantity=data.get('quantity'),
                                                                unit=data.get('unit'), user_id=data.get('user'),
                                                                recip_ingredient=recip_ingredient,
                                                                expiration_date=data.get('expiration_date'))
            fridge_ingredient.save()
            serializer = FridgeIngredientSerializer(fridge_ingredient)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class RecommendationsAPIView(APIView):
    permission_classes = []

    def get(self, request):
        user = CustomUser.objects.get(id=1)
        recipes = get_recipe_suggestion(user.get_user_products_names_list())
        return Response(data=recipes, status=status.HTTP_200_OK)


@login_required()
def fridge(request):
    ingredients = RecipIngredient.objects.all()
    fridge_ingredients = FridgeIngredient.objects.filter(recip_ingredient_id=request.id)
    return render(request, 'fridge.html',
                  context={'user': request.user, 'ingredients': ingredients, 'fridge_ingredients': fridge_ingredients})



def add_food_to_fridge(request):
    if request.method == 'POST':
        data = request.POST
        try:
            existing_item = FridgeIngredient.objects.get(name=data.get('food_name'))
        except:
            existing_item = None
        if existing_item:
            print(existing_item)
            existing_item.quantity += int(data.get('quantity'))
            existing_item.save()
            return Response(FridgeIngredientSerializer(existing_item), status=status.HTTP_200_OK)
        else:
            recip_ingredient = RecipIngredient.objects.get(name=data.get('food_name'))
            fridge_ingredient = FridgeIngredient.objects.create(name=data.get('food_name'), quantity=data.get('quantity'),
                                                            unit=data.get('unit'), user_id=data.get('user'), recip_ingredient=recip_ingredient,
                                                            expiration_date=data.get('expiration_date'))
            fridge_ingredient.save()
            serializer = FridgeIngredientSerializer(fridge_ingredient)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)



def decode_barcode(request):
    barcode = get_barcode_from_image(request.FILES['image'])
    food_name = get_food_title(barcode)
    res = {"data": food_name}
    return HttpResponse(str(res))