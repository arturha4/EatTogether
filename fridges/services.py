from .models import *


def recipes_to_dict():
    res = {"recipes": []}
    for recip in Recip.objects.all():
        res['recipes'].append({"recip_name": recip.name, "ingredients": recip.get_name_of_ingredients()})
    return res


def find_food_to_cook():
    user_ingredients = input('Введите продукты, которые есть у вас, через запятую: ').split(',')

    # Создаем список для сортировки рецептов по количеству недостающих ингредиентов
    sorted_recipes = []

    # Перебираем все рецепты
    for recipe, ingredients in recipes_to_dict()['recipes']:
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
