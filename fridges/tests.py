import datetime

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from cooperation.models import Cooperation
from users.models import CustomUser


class CooperationTests(APITestCase):
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