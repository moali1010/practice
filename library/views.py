from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from library.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm


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
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


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
