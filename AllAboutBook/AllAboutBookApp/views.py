from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Book, ListRead, Review
from .serializers import BookSerializer, BookSerializerView, ListReadSerializer, ListReadSerializerView, \
    ListReadSerializerUpdate, ReviewSerializer, ReviewSerializerView, ReviewSerializerUpdate



# Create your views here.

@api_view(['GET'])
def list_Book(request: Request):
    """ display all books avalible """
    books = Book.objects.all()
    dataResponse = {
        "msg": "List of All books",
        "Book": BookSerializerView(instance=books, many=True).data
    }
    return Response(dataResponse)



@api_view(['GET'])
def search(request: Request, name_book):
    """ The user and the author can search for a specific book """
    Book_filter = Book.objects.filter(name_book=name_book)
    dataResponse = {
        "msg": "you search book :",
        "Books": BookSerializerView(instance=Book_filter, many=True).data
    }
    return Response(dataResponse)


""" Author operations """


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_Book(request: Request):
    """ The author has permission to add a book from this function """
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




@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_book(request: Request, book_id):
    """ The author has permission to update a book from this function """
    if not request.user.is_authenticated or not request.user.has_perm('AllAboutBookApp.change_book'):
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        request.data["user"] = request.user.id
        book = Book.objects.get(id=book_id)
        if book.user.id == request.user.id:
            updated_book = BookSerializer(instance=book, data=request.data)
            if updated_book.is_valid():
                updated_book.save()
                responseData = {
                    "msg": "updated successefully"
                }
                return Response(responseData)
            else:
                print(updated_book.errors)
                return Response({"msg": "bad request.."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"msg": "Can't update..because the book is not found!"})


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_book(request: Request, book_id):
    """ The author has permission to delete a book from this function """
    if not request.user.is_authenticated or not request.user.has_perm('AllAboutBookApp.delete_book'):
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        book = Book.objects.get(id=book_id)
        if book.user.id == request.user.id:
            book.delete()
            return Response({"msg": "Deleted Successfully"})
        else:
            return Response({"msg": "Not Allowed.."})
    except:
        return Response({"msg": "Can't delete book..because the book is not found..!"})







"""" user operations """

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_in_ListRead(request: Request):
    """ The user can add a book in list from this function """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    request.data["user"] = request.user.id
    new_book = ListReadSerializer(data=request.data)
    if new_book.is_valid():
        new_book.save()
        dataResponse = {
            "msg": "The book has been successfully added to the list",
            "Book": new_book.data
        }
        return Response(dataResponse)
    else:
        print(new_book.errors)
        dataResponse = {"msg": "Can't add..because the book is not found!"}
        return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def ListReads(request: Request):
    """ display all book in the list """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    listRead = ListRead.objects.filter(user=request.user.id)
    print(request.user.id)
    if listRead.exists():
        dataResponse = {
                "msg": "List Read :",
                "ListRead:": ListReadSerializerView(instance=listRead, many=True).data
        }
        return Response(dataResponse)
    else:
        return Response({"msg": "You dont have books in list.."})




@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_ListRead(request: Request, ListRead_id):
    """ The user can update a book in list from this function """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
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
                return Response({"msg": "bad request.."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"msg": "Can't update..because the book is not found!"})




@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_ListRead(request: Request, ListRead_id):
    """ The user can delete a book from list from this function """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        listRead = ListRead.objects.get(id=ListRead_id)
        if listRead.user.id == request.user.id:
            listRead.delete()
            return Response({"msg": "Deleted Successfully"})
        else:
            return Response({"msg": "Not Allowed.."})
    except:
        return Response({"msg": "Can't delete..because the book is not found!"})


""" Review oprations """

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_Review(request: Request):
    """ The user can add review on the a book from this function """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    request.data["user"] = request.user.id
    new_review = ReviewSerializer(data=request.data)
    if new_review.is_valid():
        new_review.save()
        dataResponse = {
            "msg": "Add review Successfully",
            "Book": new_review.data
        }
        return Response(dataResponse)
    else:
        print(new_review.errors)
        dataResponse = {"msg": "Can't add review..because the book is not found..!"}
        return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def ListReads_Review(request: Request):
    """ display books with review in list """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    review = Review.objects.filter(user=request.user.id)
    print(request.user.id)
    if review.exists():
        dataResponse = {
            "msg": "List Read :",
            "ListRead:": ReviewSerializerView(instance=review, many=True).data
        }
        return Response(dataResponse)
    else:
        return Response({"msg": "You dont have review in book.."})




@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_review(request: Request, ListRead_id):
    """ The user can update on review a book from this function """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        review = Review.objects.get(id=ListRead_id)
        if review.user.id == request.user.id:
            updated_review = ReviewSerializerUpdate(instance=review, data=request.data)
            if updated_review.is_valid():
                updated_review.save()
                responseData = {
                    "msg": "updated successefully"
                }
                return Response(responseData)
            else:
                print(updated_review.errors)
                return Response({"msg": "bad request.."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"msg": "Can't update review..because the book is not found..!"})





@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_review(request: Request, ListRead_id):
    """ The user can delete review a book from this function """
    if not request.user.is_authenticated:
        return Response({"msg": "Not Allowed"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        review = Review.objects.get(id=ListRead_id)
        if review.user.id == request.user.id:
            review.delete()
            return Response({"msg": "Deleted Successfully"})
        else:
            return Response({"msg": "Not Allowed.."})
    except:
        return Response({"msg": "Can't delete review..because the book is not found..!"})
