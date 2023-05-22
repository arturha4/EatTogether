from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.serializers import SignUpSerializer


class RegisterView(APIView):
    permission_classes = []

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        Возвращает email юзера и 201 статус, если регистрация прошла успешно
        :param request:
        :return:
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'email': serializer.data['email']}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('events/home/')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email уже зарегистрирован!')
            return redirect('/signup')
        else:
            user = CustomUser.objects.create_user(email=email, password=password, firstname=first_name,
                                                  lastname=last_name)
            user.save()
            auth.login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('/events/home')
    else:
        return render(request, 'registration.html')


@login_required()
def home(request):
    return render(request, 'home.html')

@login_required()
def profile(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        user.room_number = request.POST.get('room_number')
        user.save()
        return redirect('profile')
    else:
        return render(request, 'profile.html', context={'user': request.user})

@login_required()
def logout_user(request):
    logout(request)
    return redirect('/signin')


def find_closed_neighbours(request):
    pass
