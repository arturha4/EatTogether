import datetime

from fridges.models import FridgeIngredient


def check_expired_products():
    for fridge in FridgeIngredient.objects.all():
        current_time = datetime.datetime.now() + datetime.timedelta(days=1)
        expiration_time = fridge.expiration_date

        if expiration_time <= current_time.date():
            print(f"Продукт {fridge.name} испортился или испортится в течение 24 часов. Срок годности до:{fridge.expiration_date}")
        else:
            print(f"Продукт {fridge.name} не испортится в течение 24 часов. Срок годности до:{fridge.expiration_date}")
    print('_________________________________________________________________________________________')
