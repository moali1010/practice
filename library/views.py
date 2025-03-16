import time
import asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from library.forms import SignUpForm, BookForm
from library.models import Book, Author, Profile
# from library.permissions import IsFromSpecificCountry, IsBookAuthorOrAdmin
from library.permissions import IsAuthorOrAdmin, IsOwnerOrReadOnly, OnlyAdminCanEdit
from library.serializers import BookSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
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
@api_view(['GET', 'PUT', "DELETE", "POST"])
def book_detail_update_delete(request, book_id):
    # book = Book.objects.get(id=book_id)
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'GET':
        serializer = BookSerializer(instance=book)
        # response = {"id": book.id, "pages": book.pages_count}
        # return Response(data=response)
        data = serializer.data
        return Response({'data': data})

    if request.method == 'DELETE':
        book.delete()
        return HttpResponse('Book deleted')

    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        # payload = json.loads(request.body)
        # pages_count = payload.get('pages_count', None)
        # if pages_count is None:
        #     return HttpResponse('Pages count is required!')
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=400)
        # Book.objects.create(pages_count=serializer.data['pages_count'])
        serializer.save()
        return HttpResponse('Book updated successfully!')

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
        if request.user.is_authenticated:
            return Response({'msg': 'Hello POST!'})


class HelloAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(data={'message': f"Hello {request.user.username}!"})


# @api_view(['POST'])
# def new_login_rest(request):
#     from rest_framework.authtoken.models import Token
#
#     user = User.objects.get(username=request.data['username'])
#     if user.check_password(request.data['password']):
#         token = Token.objects.create(user=user, key=Token.generate_key())
#
#     return HttpResponse({'token': token.key})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_logout(request):
    # if not request.user.is_authenticated:
    #     return Response({'msg': 'You are not logged in'})
    # request.user.auth_token.delete()
    # return Response({'msg': 'You are logged out'})
    request.user.auth_token.delete()
    return Response({'msg': 'You are logged out'}, status=200)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': f"Bye {request.user.username}!"})


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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookListCreateAPIView2(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # get, put, delete
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListCreateAPIView3(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# curl -H "Authorization: Bearer your_access_token" http://<your_domain>/api/some_protected_view/

# class BookListView(APIView):  # فقط کاربران لاگین‌شده
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         ...  # لیست کتاب‌ها را برگردان

# class AuthorAdminView(APIView):  # فقط ادمین‌ها
#     permission_classes = [IsAdminUser]
#
#     def delete(self, request, author_id):
#         ...  # حذف نویسنده (فقط ادمین)

# class IranBooksView(APIView):
#     permission_classes = [IsAuthenticated, IsFromSpecificCountry]
#
#     def get(self, request):
#         ...  # لیست کتاب‌های مربوط به ایران

# class BookDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated, IsBookAuthorOrAdmin]
#
#     def perform_update(self, serializer):
#         serializer.save()

# class CustomPermission(BasePermission):  # ترکیب پرمیشن‌ها
#     def has_permission(self, request, view):
#         user = request.user
#         return (
#                 user.is_authenticated and
#                 (user.profile.country == "Iran" or user.is_staff)
#         )

# # ارتباط بین مدل‌ها و پرمیشن‌ها
# class SameCountryBooksOnly(BasePermission):  # دسترسی به کتاب‌ها بر اساس کشور کاربر
#     def has_permission(self, request, view):
#         user_country = request.user.profile.country
#         author_country = Author.objects.filter(books__id=view.kwargs['book_id']).first().country
#         return user_country == author_country


class BookUpdateView(UpdateAPIView):  # ویرایش کتاب فقط توسط نویسنده یا ادمین
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]

    def perform_update(self, serializer):
        serializer.save()


# پرمیشن‌های کلی (Global Permissions)
class BookDetailAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)  # فقط کاربران لاگین شده می‌توانند جزئیات کتاب را ببینند.
    # permission_classes = (OnlyAdminCanEdit,)


# پرمیشن‌های سطح شیء (Object-level Permissions)
class ProfileDetailAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        # فرض کنید می‌خواهیم فقط پروفایل کاربر درخواست دهنده برگردانده شود.
        return self.request.user.profile


def get_books():
    print("getting books ....")
    time.sleep(2)
    qs = Book.objects.all()
    print(qs)
    print("all books fetched")


def get_authors():
    print("getting authors ...")
    time.sleep(5)
    qs = Author.objects.all()
    print(qs)
    print("all authors fetched")


@sync_to_async
def get_books_async():
    print("getting books ....")
    time.sleep(2)
    qs = Book.objects.all()
    print(qs)
    print("all books fetched")


@sync_to_async
def get_authors_async():
    print("getting authors ...")
    time.sleep(5)
    qs = Author.objects.all()
    print(qs)
    print("all authors fetched")


def sync_view(request):
    start_time = time.time()
    get_books()
    get_authors()
    total = time.time() - start_time
    return HttpResponse(f"time taken {total}")


async def async_view(request):
    start_time = time.time()
    ### approach 1
    # movie_task = asyncio.ensure_future(get_books_async())
    # theatre_task = asyncio.ensure_future(get_authors_async())
    # await asyncio.wait([movie_task, theatre_task])
    ### approach 2 using gather
    await asyncio.gather(get_books_async(), get_authors_async())
    total = time.time() - start_time
    return HttpResponse(f"time taken async {total}")
