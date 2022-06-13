from django.urls import path
from . import views



urlpatterns = [
    path("list_Book/", views.list_Book, name="list_Book"),
    path("add_Book/", views.add_Book, name="add_Book"),
    path("update_book/<name_book>", views.update_book, name="update_book"),
    path("delete_book/<name_book>", views.delete_book, name="delete_book"),
    path("search/<name_book>", views.search, name="search"),
    path("add_in_ListRead/", views.add_in_ListRead, name="add_in_ListRead"),
    path("ListReads/", views.ListReads, name="ListReads"),
    path("update_ListRead/<ListRead_id>", views.update_ListRead, name="update_ListRead"),
    path("delete_ListRead/<ListRead_id>", views.delete_ListRead, name="delete_ListRead"),

]