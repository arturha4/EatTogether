from .models import FridgeIngredient
from apscheduler.schedulers.background import BackgroundScheduler


def check_expired_products():
    products = FridgeIngredient.objects.all()
    for pr in products:
        pr.delete()
    print("Deleted")
