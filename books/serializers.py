import json
import logging

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Book, User, Author
from books import validators as book_validators
from books import errors as err
logger = logging.getLogger(__name__)

#: Author serializers


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer to return only author details
    """
    class Meta:
        model = Author
        fields = ('uid', 'username')

#: Book serializer


class BookListSerializer(serializers.ModelSerializer):
    """
    Model serializer for listing books
    """

    authors = AuthorSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ('id', 'isbn', 'title', 'status', 'authors')


#: User serializers


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Model serializer for updating wish list item
    """
    wishlist = serializers.ListField(default='[]')

    class Meta:
        model = User
        fields = ('uid', 'wishlist')

    def validate(self, attrs):
        """
        To validate the wish list items
        :param attrs:
        :return:
        """
        #: Convert the string passed.
        wishlist_items = attrs.get('wishlist')
        for book_id in wishlist_items:
            #: Validate the book ids passed to ensure they are real ones.
            book_instance = book_validators.validate_book_exists_based_on_id(book_id)
            if self.context['request'].data['action'] == 'add':
                #: We need to check whether book is unavailable before adding it to wish list
                if not book_validators.validate_books_status(book_instance):
                    raise err.ValidationError('Book is already available . You can lent it now.', 400)
                #: We need to check book is already in wish list if it exist no need to add once again
                if book_validators.check_book_exist_in_wishlist(book_instance, self.instance):
                    raise err.ValidationError('Book already exist in your wish list', 400)
            else:
                #: We need to check book is already in wish list inorder to remove it
                if not book_validators.check_book_exist_in_wishlist(book_instance, self.instance):
                    raise err.ValidationError('Book not exist in your wish list', 400)
        return attrs

    def update(self, instance, validated_data):
        #: Get the book objects for wishlisted items
        wishlisted_books = Book.objects.filter(id__in=validated_data['wishlist'])
        if self.context['request'].data['action'] == 'add':
            #: ADD books to the user wishlist
            instance.wishlist.add(*wishlisted_books)
        else:
            instance.wishlist.remove(*wishlisted_books)
        instance.save()
        return instance

#: Book Serializers


class BookStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Model serializer for updation book status
    """
    status = serializers.CharField()


    def validate(self, attrs):
        """
        To validate the wish list items
        :param attrs:
        :return:
        """
        return attrs

    def update(self, instance, validated_data):
        #: Get the status value
        status = validated_data['status']
        #: Change the instance status
        instance.status = status
        instance.save()
        return instance

    class Meta:
        model = Book
        fields = ('id', 'title', 'status')


class BookAmazonUpdateSerializer(serializers.ModelSerializer):
    """
    Model serializer to update amazon's id of book
    """
    amazon_id = serializers.CharField()

    def validate(self, attrs):
        """
        To validate the wish list items
        :param attrs:
        :return:
        """
        return attrs

    def update(self, instance, validated_data):
        #: Get the status value
        status = validated_data['amazon_id']
        #: Change the instance status
        instance.amazon_id = status
        instance.save()
        return instance

    class Meta:
        model = Book
        fields = ('id', 'amazon_id')