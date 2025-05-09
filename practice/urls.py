"""
URL configuration for practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # or ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from library.views import (signup, user_list, register_user,
                           login_user, logout_user, login_user2,
                           change_password, logout_user2, login_first,
                           add_book, change_book, view_book, delete_book,
                           book_detail_update_delete, HelloView,
                           BookListAPIView, BookListCreateAPIView,
                           BookListCreateAPIView2, BookRetrieveUpdateDestroyAPIView,
                           new_logout, BookListCreateAPIView3, sync_view, async_view, )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/signup/', signup),
    path('user_list/', user_list),
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('library/login/', login_user2),
    path('library/change-password/', change_password),
    path('library/logout/', logout_user2),
    path('library/login-first/', login_first),
    path('library/add-book/', add_book),
    path('library/change-book/<int:book_id>/', change_book),
    path('library/view-book/<int:book_id>/', view_book),
    path('library/delete-book/<int:book_id>/', delete_book),
    path('books/<int:book_id>/', book_detail_update_delete),
    path('hello/', HelloView.as_view()),
    path('books/seri/', BookListAPIView.as_view()),
    path('book-list-create/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('book-list-create2/', BookListCreateAPIView2.as_view()),
    path('books2/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('login2/', view=obtain_auth_token),
    path('logout2/', new_logout, name='new_logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/books/', BookListCreateAPIView3.as_view()),
    path("sync_view/", sync_view),
    path("async_view/", async_view)
]
