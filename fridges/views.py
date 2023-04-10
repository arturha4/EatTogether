from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import RecipIngredient, FridgeIngredient, Fridge
from .services import recipes_to_dict

@login_required()
def fridge(request):
    user_fridge = Fridge.objects.get(customuser=request.user)
    ingredients = RecipIngredient.objects.all()
    fridge_ingredients = FridgeIngredient.objects.filter(fridge_id=user_fridge.id)
    return render(request, 'fridge.html',
                  context={'user': request.user, 'ingredients': ingredients, 'fridge_ingredients': fridge_ingredients})


@login_required()
def add_food_to_fridge(request):
    if request.method == 'POST':
        data = request.POST
        fridge = Fridge.objects.get(customuser=request.user)
        recip_ingredient = RecipIngredient.objects.get(name=data.get('food_name'))
        fridge_ingredient = FridgeIngredient.objects.create(name=data.get('food_name'), quantity=data.get('quantity'),
                                                            unit=data.get('unit'), recip_ingredient=recip_ingredient,
                                                            fridge=fridge, expiration_date=data.get('expiration_date'))
        fridge_ingredient.save()
    return redirect('/my-fridge')


def recommended_food(request):
    print(recipes_to_dict())

