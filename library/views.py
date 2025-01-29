from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from library.forms import SignUpForm


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
