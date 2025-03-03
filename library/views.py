from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from library.forms import SignUpForm, BookForm
from library.models import Book, Author
from library.serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status
import json


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


@permission_required('library.change_book', raise_exception=True)
@login_required(login_url='/library/login-first/')
@csrf_exempt
def change_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponse('Book information updated!')
        return HttpResponse(f"{form.errors}")


@permission_required('library.view_book', raise_exception=True)
@login_required(login_url='/library/login-first/')
@csrf_exempt
@api_view(['GET'])
def view_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        if request.method == 'GET':
            # book = get_object_or_404(Book, id=book_id)
            # return HttpResponse(f"{model_to_dict(book)}")
            response = {"id": book.id, "title": book.title, "author": str(book.author)}
            # return HttpResponse(json.dumps(response))
            # OR return HttpResponse(response_json, content_type='application/json'
            return Response(data=response)
    except Book.DoesNotExist:
        return HttpResponse(json.dumps({'error': 'Book not found'}), status=404)
    # return HttpResponse('Only get method allowed!')
    return HttpResponse(json.dumps({'error': 'Only GET method allowed'}), status=405)


@permission_required('library.delete_book', raise_exception=True)
@login_required(login_url='/library/login-first/')
@csrf_exempt
def delete_book(request, book_id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return HttpResponse('Book deleted successfully!')
    return HttpResponse('Only delete method allowed!')


@csrf_exempt
@api_view(['GET', 'PUT', "DELETE"])
def book_detail_update_delete(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'GET':
        response = {"id": book.id, "pages": book.pages_count}
        return Response(data=response)

    if request.method == 'DELETE':
        book.delete()
        return HttpResponse('Book deleted')

    if request.method == 'PUT':
        # print(request.data)
        # payload = json.loads(request.body)
        # pages_count = payload.get('pages', None)
        pages_count = request.data['pages']
        if pages_count is None:
            return HttpResponse("Error: number is not provided")
        book.pages_count = pages_count
        book.save()
        return HttpResponse('Book updated')

    return HttpResponse('Method not allowed')


class HelloView(APIView):
    def get(self, request):
        return Response({'msg': 'Hello GET!'})

    def post(self, request):
        return Response({'msg': 'Hello POST!'})


class BookListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data.get("title")
        author_id = data.get("author_id")
        author = Author.objects.get(id=author_id)
        print(str(author))
        pages_count = data.get("pages_count")
        publish_date = data.get("publish_date")
        book = Book.objects.create(
            title=title, author=author,
            pages_count=pages_count,
            publish_date=publish_date)  # ساختن کتاب
        serializer = BookSerializer(book)  # ترجمه به json
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookListCreateAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
