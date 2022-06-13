from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Book, ListRead
from .serializers import BookSerializer, BookSerializerView, ListReadSerializer, ListReadSerializerView, \
    ListReadSerializerUpdate


# Create your views here.


# display books
@api_view(['GET'])
def list_Book(request: Request):
    books = Book.objects.all()
    dataResponse = {
        "msg": "List of All books",
        "Book": BookSerializerView(instance=books, many=True).data
    }
    return Response(dataResponse)


# Search Function
@api_view(['GET'])
def search(request: Request, name_book):
    Book_filter = Book.objects.filter(name_book=name_book)
    dataResponse = {
        "msg": "you search book :",
        "Books": BookSerializerView(instance=Book_filter, many=True).data
    }
    return Response(dataResponse)


# Author operations
# Add book
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_Book(request: Request):
    if not request.user.is_authenticated or not request.user.has_perm('AllAboutBookApp.add_book'):
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    request.data["user"] = request.user.id
    new_book = BookSerializer(data=request.data)
    if new_book.is_valid():
        new_book.save()
        dataResponse = {
            "msg": "Created Successfully",
            "Book": new_book.data
        }
        return Response(dataResponse)
    else:
        print(new_book.errors)
        dataResponse = {"msg": "couldn't create a book"}
        return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


# Update on book
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_book(request: Request, name_book):
    if not request.user.is_authenticated or not request.user.has_perm('AllAboutBookApp.change_book'):
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    request.data["user"] = request.user.id
    books = Book.objects.filter(name_book=name_book)
    if books.exists():
        book = Book.objects.get(name_book=name_book)
        updated_book = BookSerializer(instance=book, data=request.data)
        if updated_book.is_valid():
            updated_book.save()
            responseData = {
                "msg": "updated successefully"
            }

            return Response(responseData)
        else:
            print(updated_book.errors)
            return Response({"msg": "bad request, cannot update"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "Can't update..Because the book is not available!"})


# delete book
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_book(request: Request, name_book):
    if not request.user.is_authenticated or not request.user.has_perm('AllAboutBookApp.delete_book'):
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    book = Book.objects.filter(name_book=name_book)
    if book.exists():
        book.delete()
        return Response({"msg": "Deleted Successfully"})
    else:
        return Response({"msg": "Can't delete..Because the book is not available!"})


################################################# user operations ##########################################

# add book in the list
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_in_ListRead(request: Request):
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    request.data["user"] = request.user.id
    new_book = ListReadSerializer(data=request.data)
    if new_book.is_valid():
        new_book.save()
        dataResponse = {
            "msg": "Add in List Read Successfully",
            "Book": new_book.data
        }
        return Response(dataResponse)
    else:
        print(new_book.errors)
        dataResponse = {"msg": "couldn't add a book in list read..because I couldn't find the book"}
        return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


# display all book in the list
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def ListReads(request: Request):
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    listRead = ListRead.objects.all()
    dataResponse = {
        "msg": "List Read :",
        "ListRead:": ListReadSerializerView(instance=listRead, many=True).data
    }
    return Response(dataResponse)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_ListRead(request: Request, ListRead_id):
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    listRead = ListRead.objects.get(id=ListRead_id)

    if listRead.user.id == request.user.id:
        updated_book = ListReadSerializerUpdate(instance=listRead, data=request.data)
        if updated_book.is_valid():
            updated_book.save()
            responseData = {
                "msg": "updated successefully"
            }
            return Response(responseData)
        else:
            print(updated_book.errors)
            return Response({"msg": "bad request, cannot update"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)


# delete book from list
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_ListRead(request: Request, ListRead_id):
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    #listRead = ListRead.objects.filter(id=ListRead_id)


    try:
        listRead = ListRead.objects.get(id=ListRead_id)
        if listRead.user.id == request.user.id:
            listRead.delete()
            return Response({"msg": "Deleted Successfully"})
        else:
            return Response({"msg": "Not Allowed.."})
    except:
        return Response({"msg": "cant delete..book not avalible"})


