from .models import *
from pyzbar.pyzbar import decode
from io import BytesIO
from PIL import Image
import requests
from bs4 import BeautifulSoup

from .serializers import RecipSerializer


def get_food_title(barcode: str):
    url = f'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=+{barcode}'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for title in soup.find('title'):
        if title.get_text().split(' - ')[0][:5] == 'Поиск':
            return 'Для данного товара ифнормация в базе найдена не была'
    return title.get_text().split(' - ')[0]


def get_recipes_dict():
    recipes = {}
    for recip in Recip.objects.all():
        recipes[recip.name] = recip.get_name_of_ingredients()
    return recipes


def get_barcode_from_image(image):
    img = Image.open(BytesIO(image.read()))
    barcodes = decode(img)
    for barcode in barcodes:
        return barcode.data.decode('utf-8')

#
# def find_food_to_cook(input_food):
#     # users_ingredients это обьекты FridgeIngredient нашего пользователя или кооперации нескольких пользователей
#     user_ingredients = input_food
#     # Создаем список для сортировки рецептов по количеству недостающих ингредиентов
#     sorted_recipes = []
#     # Перебираем все рецепты
#     for recipe, ingredients in get_recipes_dict().items():
#         # Находим ингредиенты рецепта, которых нету среди имеющихся продуктов
#         missing_ingredients = [ingredient for ingredient in ingredients if ingredient not in user_ingredients]
#         # Если количество недостающих ингредиентов равно 0, добавляем рецепт в список возможных рецептов со значением "список ингредиентов пуст"
#         if len(missing_ingredients) == 0:
#             sorted_recipes.append((recipe, "Нет недостающих ингредиентов"))
#         # Если некоторых ингредиентов от рецепта не хватает, добавляем рецепт в список со списком недостающих ингредиентов
#         else:
#             sorted_recipes.append((recipe, missing_ingredients))
#     # Сортируем список по количеству недостающих ингредиентов
#     sorted_recipes = sorted(sorted_recipes, key=lambda x: len(x[1]))
#     # Выводим список возможных рецептов вместе с перечнем недостающих продуктов
#     if sorted_recipes:
#         print('Вы можете приготовить следующие блюда:')
#         for recipe, missing_ingredients in sorted_recipes:
#             if missing_ingredients == "Нет недостающих ингредиентов":
#                 print(recipe)
#             else:
#                 print(recipe + " - не хватает: " + ", ".join(missing_ingredients))
#     else:
#         print('К сожалению, вы не можете приготовить ни одного блюда')


def get_recipe_suggestion(input_food):
    user_ingredients = input_food
    sorted_recipes = []
    for recipe, ingredients in get_recipes_dict().items():
        missing_ingredients = [ingredient for ingredient in ingredients if ingredient not in user_ingredients]
        if len(missing_ingredients) == 0:
            sorted_recipes.append({"recipe": recipe, "missing_ingredients": []})
        else:
            sorted_recipes.append({"recipe": recipe, "missing_ingredients": missing_ingredients})
    sorted_recipes = sorted(sorted_recipes, key=lambda x: len(x["missing_ingredients"]))
    result = {"partially": [],
              "possible": []}
    if sorted_recipes:
        for recipe in sorted_recipes:
            if not recipe["missing_ingredients"]:
                result["possible"].append(RecipSerializer(Recip.objects.get(name=recipe["recipe"])).data)
            else:
                result["partially"].append({"name": recipe["recipe"], 'missed_ingredients': recipe["missing_ingredients"],
                                         'existing_ingredients': set(
                                             Recip.objects.get(name=recipe["recipe"]).get_name_of_ingredients()) - set(
                                             recipe["missing_ingredients"])})
        return result
    result = {'error': 'К сожалению, вы не можете приготовить ни одного блюда'}
    return result
