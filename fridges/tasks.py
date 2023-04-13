import datetime
import random

from cooperation.models import Cooperation,CustomUser


def check_expired_products():
    for user in CustomUser.objects.all():
        cooperation=Cooperation.objects.create(title=str(random.randint(100,200000)), description=str(random.randint(100,200000)),
                               date=datetime.datetime.now(), creator=user)
        cooperation.save()
        print(cooperation.title + "- created")
