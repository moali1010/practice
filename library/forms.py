from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from library.models import Profile, Book


class SignUpForm(UserCreationForm):
    country = (forms.CharField(max_length=100))

    class Meta:
        model = User
        fields = ('username', 'country', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.create(
            user=user, country=self.data['country']
        )
        return user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publish_date', 'pages_count', 'author')
