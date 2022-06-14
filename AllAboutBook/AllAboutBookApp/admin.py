from django.contrib import admin
from .models import Book, ListRead, Review


class book(admin.ModelAdmin):
    list_display = ('name_book', 'Discrption_book', 'user', 'Date_of_publish',)


class listRead(admin.ModelAdmin):
    list_display = ('book', 'start_date', 'finish_date', 'progression_level', 'user')


class review(admin.ModelAdmin):
    list_display = ('listread', 'date', 'comment', 'user')


# Register your models here.
admin.site.register(Book, book)
admin.site.register(ListRead, listRead)
admin.site.register(Review, review)
