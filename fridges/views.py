import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.models import CustomUser
from .models import RecipIngredient, FridgeIngredient
from .services import find_food_to_cook


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


def recommended_food(request):
    names_list = ['Иванов Иван', 'Петров Петр', 'Сидоров Сидор', 'Кузнецова Екатерина', 'Соловьева Вера',
                  'Титова Анна', 'Медведева Анастасия', 'Лебедева Ольга', 'Семенова Валентина', 'Никитина Ирина',
                  'Маркова Дарья', 'Романова Елена', 'Смирнова Александра', 'Федорова Ангелина', 'Матвеева Алена',
                  'Михайлова Ольга', 'Новикова Юлия', 'Козлов Ярослав', 'Васильев Артем', 'Григорьев Николай',
                  'Горбачев Егор', 'Лапин Артур', 'Карасев Александр', 'Кравец Владислав', 'Смирнов Егор',
                  'Попов Игорь', 'Воронина Евгения', 'Соколова Оксана', 'Полякова Татьяна', 'Богданова Екатерина',
                  'Терехова Александра', 'Белова Анастасия', 'Денисова Анна', 'Кудряшова Юлия', 'Жукова Софья',
                  'Рябова Елена', 'Лазарева Дарья', 'Орлова Марина', 'Комарова Ирина', 'Мельникова Вера',
                  'Громова Анастасия', 'Антонова Анна', 'Бурова Анна', 'Комиссарова Евгения', 'Логинова Ксения',
                  'Пахомова Юлия', 'Тимофеева Анастасия', 'Шестакова Ольга', 'Фадеева Елена', 'Петухова Елена']
    for i in names_list:
        user = CustomUser.objects.create(email=str(random.randint(1,5344323))+"@mail.ru", firstname=i.split()[0],
                                  lastname=i.split()[1], room_number=random.randint(100,500))
        user.save()
