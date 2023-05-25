import datetime

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from .models import FridgeIngredient, Recip, RecipIngredient
from users.models import CustomUser


class FridgeTests(APITestCase):
    client = APIClient()

    def authenticate(self):
        self.client.post(reverse('signup'), {'email': 'test@mail.ru',
                                             'firstname': 'test',
                                             'lastname': 'test',
                                             'password': 'qwertyui',
                                             'password2': 'qwertyui'})
        response = self.client.post(reverse('token_obtain_pair'), {'email': 'test@mail.ru',
                                                                   'password': 'qwertyui'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    @staticmethod
    def create_and_get_user(email='sad@mail.ru'):
        user = CustomUser.objects.create(email=email,
                                     firstname='art',
                                     lastname='dav',
                                     room_number=444,
                                     password='qwertyqwerty')
        user.save()
        return user

    def test_add_new_food_to_fridge(self):
        self.authenticate()
        url = reverse('food')
        user1 = FridgeTests.create_and_get_user()
        ri = RecipIngredient.objects.create(name='Яйца')
        ri.save()
        json_data = {
            "food_name": "Яйца",
            'quantity': 10,
            'unit': 'штук',
            'expiration_date': datetime.date(2023, 5, 29),
            'user': user1.id,
        }
        response = self.client.post(url, json_data)
        self.assertEqual(response.data.get('name'), user1.products.first().name)

    def test_add_existing_food_to_fridge(self):
        self.authenticate()
        url = reverse('food')
        user1 = FridgeTests.create_and_get_user()
        ri = RecipIngredient.objects.create(name='Яйца')
        ri.save()
        fridge_ingredient = FridgeIngredient.objects.create(name='Яйца',
                                                            quantity=2,
                                                            unit='штук', user_id=user1.id,
                                                            recip_ingredient=ri,
                                                            expiration_date=datetime.date(2023, 5, 29))
        fridge_ingredient.save()
        json_data = {
            "food_name": "Яйца",
            'quantity': 10,
            'unit': 'штук',
            'expiration_date': datetime.date(2023, 5, 29),
            'user': user1.id
        }
        response = self.client.post(url, json_data)
        self.assertEqual(int(float(response.data.get('quantity'))), 12)

