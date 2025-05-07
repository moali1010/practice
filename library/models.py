import datetime
from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100)

    def is_young(self):
        return self.birth_date > datetime.date(1990, 1, 1)

    def is_old(self):
        return self.birth_date < datetime.date(1960, 1, 1)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    publish_date = models.DateField()
    pages_count = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     country = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=50, blank=True, null=True)


# class Cake(models.Model):
#     sauce = models.CharField(default="Chocolate", max_length=20)

"""
from django.db import migrations
from django.db.models import CharField, Value, F
from django.db.models.functions import Concat, Replace


def alter_names_of_sauces(apps, schema_editor):
    Cake = apps.get_model('app', 'Cake')

    Cake.objects.annotate(
        new_sauce_name=Concat(
            F('sauce'), Value(' Sauce'), output_field=CharField()
        )
    ).update(sauce=F('new_sauce_name'))


def reverse_alter_names_of_sauces(apps, schema_editor):
    Cake = apps.get_model('app', 'Cake')

    Cake.objects.update(
        sauce=Replace('sauce', text=Value(' Sauce'), replacement=Value(''))
    )


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            alter_names_of_sauces,
            reverse_code=reverse_alter_names_of_sauces
        ),
    ]
"""
