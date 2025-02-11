from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    publish_date = models.DateField()
    pages_count = models.IntegerField()
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.CASCADE
    )
    hidden = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("hide_book", "Can make book hidden"),
        ]

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100)

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     country = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=50, blank=True, null=True)
