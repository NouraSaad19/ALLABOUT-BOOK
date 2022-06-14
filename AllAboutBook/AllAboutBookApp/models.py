from time import timezone

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    name_book = models.CharField(max_length=100)
    Discrption_book = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #name_author = models.CharField(max_length=100)
    Date_of_publish = models.DateField()


class ListRead(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField()
    finish_date = models.DateField()
    progression_level = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    listread = models.ForeignKey(ListRead, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField()








