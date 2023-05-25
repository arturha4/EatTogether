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

    @staticmethod
    def create_and_get_user(email='sad@mail.ru'):
        user = CustomUser.objects.create(email=email,
                                         firstname='art',
                                         lastname='dav',
                                         room_number=444,
                                         password='qwertyqwerty')
        user.save()
        return user

    @staticmethod
    def create_and_get_cooperation():
        c = Cooperation.objects.create(title='Варим борщ',
                                       description='Нужна картошка и свекла, мясо есть',
                                       date=datetime.datetime.now(),
                                       creator_id=1)
        c.save()
        return c

    def test_create_cooperation(self):
        self.authenticate()
        url = reverse('cooperation')
        data = {'title': "Варим борщ",
                'description': 'Нужна картошка и свекла, мясо есть',
                'date': datetime.datetime.now(),
                'creator': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_second_cooperation_create(self):
        self.authenticate()
        url = reverse('cooperation')
        CooperationTests.create_and_get_cooperation()
        data = {'title': "Варим борщ",
                'description': 'Нужна картошка и свекла, мясо есть',
                'date': datetime.datetime.now(),
                'creator': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_join_to_cooperation(self):
        self.authenticate()
        cooperation = CooperationTests.create_and_get_cooperation()
        user1, user2 = CooperationTests.create_and_get_user(),\
                       CooperationTests.create_and_get_user(email='artdav@mail.ru')
        url = reverse('cooperation-detail', kwargs={'pk': cooperation.id})
        data = {'participants': [user1.id, user2.id]}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['participants'], list(cooperation.participants.values_list('id', flat=True)))

    def test_user_leave_to_cooperation(self):
        self.authenticate()
        cooperation = CooperationTests.create_and_get_cooperation()
        user1, user2 = CooperationTests.create_and_get_user(),\
                       CooperationTests.create_and_get_user(email='artdav@mail.ru')
        url = reverse('cooperation-detail', kwargs={'pk': cooperation.id})
        data = {'participants': [user1.id, user2.id]}
        self.client.put(url, data=data, format='json')
        print(Cooperation.objects.get(id=cooperation.id).participants)
        url = reverse('leave-event', kwargs={'pk': cooperation.id})
        response = self.client.post(url, data=data, format='json')
        print(Cooperation.objects.get(id=cooperation.id).participants)
        self.assertEqual(1, status.HTTP_201_CREATED)
        self.assertEqual(response.data['participants'], list(cooperation.participants.values_list('id', flat=True)))
