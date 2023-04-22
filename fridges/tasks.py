import datetime

from fridges.models import FridgeIngredient
from cooperation.models import ProductExpiredNotification


def check_expired_products():
    for product in FridgeIngredient.objects.all():
        current_datetime = datetime.datetime.now() + datetime.timedelta(days=1)
        current_date = current_datetime.date()
        if product.expiration_date == current_date:
            if not ProductExpiredNotification.objects.filter(user=product.user,
                                                             text=f"Продукт {product.name} cкоро испортится. Срок годности до {product.expiration_date}"):
                notification = ProductExpiredNotification.objects.create(user=product.user,
                                                                         text=f"Продукт {product.name} скоро испортится. Срок годности до {product.expiration_date}")
                notification.save()
        if product.expiration_date <= datetime.datetime.now().date():
            if not ProductExpiredNotification.objects.filter(user=product.user,
                                                             text=f"{product.name} испортился. Срок годности истекает {product.expiration_date}"):
                notification = ProductExpiredNotification.objects.create(user=product.user,
                                                          text=f"{product.name} испортился. Срок годности истеквет {product.expiration_date}")
                notification.save()

