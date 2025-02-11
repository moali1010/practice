from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from library.forms import SignUpForm, BookForm
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


@csrf_exempt
def login_user2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse('Login completed!')
        return HttpResponse('Wrong password/username')

    return HttpResponse('Please login with post method')


def logout_user(request):
    if request.method == 'GET' and request.user.is_authenticated:
        logout(request)
        return HttpResponse('You are logged out!')
    return HttpResponse('Method NOT allowed!')


@csrf_exempt
def logout_user2(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Please login first')

        logout(request)
        return HttpResponse('Logout successfully')

    return HttpResponse('Only post method allowed')


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Please login first')

        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            return HttpResponse('Wrong old password')

        if new_password1 != new_password2:
            return HttpResponse('Entered passwords are not identical')

        request.user.set_password(new_password1)
        request.user.save()

        return HttpResponse('Password changed successfully!')

    return HttpResponse('Only post method allowed')


# Authentication
def login_first(request):
    return HttpResponse('Please login first')


@csrf_exempt
@login_required(login_url='/library/login-first/')
def logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse('Logout successfully')

    return HttpResponse('Only post method allowed')


# Permission:
# library.add_book, library.change_book,
# library.delete_book, library.view_book
@permission_required('library.add_book', raise_exception=True)
@login_required(login_url='/library/login-first/')
@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Book added successfully')

        return HttpResponse(f"{form.errors}")

    return HttpResponse('Only post method allowed')
