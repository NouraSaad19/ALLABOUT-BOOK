from rest_framework import serializers
from .models import Book , ListRead , Review
from django.contrib.auth.models import User




class UserSerializerView(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


#display all information with username
class BookSerializerView(serializers.ModelSerializer):
    user = UserSerializerView()
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1

#display oall information book
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

class ListReadSerializerView(serializers.ModelSerializer):
    book = BookSerializerView()
    class Meta:
        model = ListRead
        fields = '__all__'

class ListReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListRead
        fields = '__all__'

class ListReadSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = ListRead
        exclude = ["book", "user"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializerView(serializers.ModelSerializer):
    listread= ListReadSerializerView()
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["listread", "user"]

