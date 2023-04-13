from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from users.models import CustomUser


def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
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
