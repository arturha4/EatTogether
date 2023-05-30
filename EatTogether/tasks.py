from __future__ import absolute_import
import datetime
from celery import shared_task
from fridges.models import FridgeIngredient
from cooperation.models import ProductExpiredNotification

@shared_task
def check_fridge_ingredients_expiration():
    fridge_ingredients = FridgeIngredient.objects.all()
    today = datetime.date.today()
    for fridge_ingredient in fridge_ingredients:
        if fridge_ingredient.expiration_dates.filter(expiration_date__lt=today).exists():
            notification = ProductExpiredNotification.objects.create(
                user=fridge_ingredient.user,
                message=f'{fridge_ingredient.name} has expired'
            )
            notification.save()
