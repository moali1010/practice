from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from library.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                'User created successfully!'
            )
        return HttpResponse(f"{form.errors}")
    return HttpResponse('Only post method allowed!')


def user_list(request):
    if request.user.is_authenticated:
        print(f"user: {request.user}")
        users = User.objects.all()
        return render(request, 'user_list.html', {
            'users': users
        })
    return HttpResponse('You are NOT logged in!')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return render(request, 'register.html', {'form': form})
        form.save()
        return HttpResponse('User Created!')

    elif request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    return HttpResponse('Method NOT allowed!')


def login_user(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {
            'form': form
        })
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse('Logged in successfully!')
        else:
            return render(request, 'login.html', {
                'form': form
            })
    else:
        return HttpResponse('Method NOT allowed!')


def logout_user(request):
    if request.method == 'GET' and request.user.is_authenticated:
        logout(request)
        return HttpResponse('You are logged out!')
    return HttpResponse('Method NOT allowed!')
