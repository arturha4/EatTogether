from .models import *
import cv2
from pyzbar.pyzbar import decode


def get_food_openfood(barcode: str):
    import requests
    from bs4 import BeautifulSoup
    url = f'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=+{barcode}'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for title in soup.find('title'):
        print(title.get_text().split(' - ')[0])


def get_recipes_dict():
    recipes = {}
    for recip in Recip.objects.all():
        recipes[recip.name] = recip.get_name_of_ingredients()
    return recipes


def parse_image():
    # загрузка изображения
    img = cv2.imread('barcode.png')

    # декодирование баркода
    barcodes = decode(img)

    # вывод результата
    for barcode in barcodes:
        print(barcode.data.decode('utf-8'))


parse_image()


def find_food_to_cook(input_food):
    # users_ingredients это обьекты FridgeIngredient нашего пользователя или кооперации нескольких пользователей
    user_ingredients = input_food
    # Создаем список для сортировки рецептов по количеству недостающих ингредиентов
    sorted_recipes = []
    # Перебираем все рецепты
    for recipe, ingredients in get_recipes_dict().items():
        # Находим ингредиенты рецепта, которых нету среди имеющихся продуктов
        missing_ingredients = [ingredient for ingredient in ingredients if ingredient not in user_ingredients]
        # Если количество недостающих ингредиентов равно 0, добавляем рецепт в список возможных рецептов со значением "список ингредиентов пуст"
        if len(missing_ingredients) == 0:
            sorted_recipes.append((recipe, "Нет недостающих ингредиентов"))
        # Если некоторых ингредиентов от рецепта не хватает, добавляем рецепт в список со списком недостающих ингредиентов
        else:
            sorted_recipes.append((recipe, missing_ingredients))
    # Сортируем список по количеству недостающих ингредиентов
    sorted_recipes = sorted(sorted_recipes, key=lambda x: len(x[1]))
    # Выводим список возможных рецептов вместе с перечнем недостающих продуктов
    if sorted_recipes:
        print('Вы можете приготовить следующие блюда:')
        for recipe, missing_ingredients in sorted_recipes:
            if missing_ingredients == "Нет недостающих ингредиентов":
                print(recipe)
            else:
                print(recipe + " - не хватает: " + ", ".join(missing_ingredients))
    else:
        print('К сожалению, вы не можете приготовить ни одного блюда')
