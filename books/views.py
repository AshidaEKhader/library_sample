import logging
import json
from django.shortcuts import render
from django.conf import settings
from .models import Book, User
from .custom_permissions import IsLibraryStaff, IsUser
from rest_framework.generics import ListAPIView, UpdateAPIView
from .utils import generate_report
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookListSerializer, UserUpdateSerializer, BookStatusUpdateSerializer, \
    BookAmazonUpdateSerializer
from books import errors as err
from books import constants as book_constants
from books import validators as book_validators
import requests

logger = logging.getLogger(__name__)
# Create your views here.


 # Book view

class BookListView(ListAPIView):
    """
        Class view to list the books
        """

    permission_classes = (IsUser, )
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        if self.request.GET:
            if self.request.GET.get('author'):
                queryset = queryset.filter(authors__username__icontains=self.request.GET.get('author'))
            if self.request.GET.get('title'):
                queryset = queryset.filter(title__icontains=self.request.GET.get('title'))
            #: To do the pagination , so that if there are 10000 accounts the api data will returns sets of 25 data,
            # and passing page will get next set of data
            page = self.paginate_queryset(queryset)
            if page is not None:
                return page
        return queryset


class WishListUpdateView(UpdateAPIView):
    """
    View model to add/ remove books to/ from  wish list
    """

    permission_classes = (IsUser, )
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        """
        :param request: {"uid": <user_uid>, "action": "add/delete", "wishlist": [<book_uid1>, <book_uid2>, etc..]
        :param args:
        :param kwargs:
        :return: {"message": "Success msg"}
        """
        # get the  user instance to be updated
        user_uid = request.data.get("uid", None)
        # Check if user exists
        user_instance = book_validators.validate_user_exists_based_on_uid(user_uid)

        serializer = self.get_serializer(user_instance, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
        except Exception as e:
            logger.error("Error inside post function inside WishListUpdateView class. ERROR {}".format(str(e)))
            raise err.ValidationError(*(e, 400))
        response = Response({"message": book_constants.WISHLIST_UPDATED}, status=status.HTTP_200_OK)
        return response


class BookStatusUpdateView(UpdateAPIView):
    """
    Model view to update book model
    """

    permission_classes = (IsLibraryStaff,)
    serializer_class = BookStatusUpdateSerializer

    def update(self, request, *args, **kwargs):
        """
        This will update the status of a book from available to borrowed or viceverca
        :param request: {"book_id": <book_id>, status="available/borrowed"}
        :param args:
        :param kwargs:
        :return: {"message": "Success msg"}
        """
        # get the  book instance to be updated
        book_id = request.data.get("book_id", None)
        # Check if book exists
        book_instance = book_validators.validate_book_exists_based_on_id(book_id)

        serializer = self.get_serializer(book_instance, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
        except Exception as e:
            logger.error("Error inside post function inside BookStatusUpdateView class. ERROR {}".format(str(e)))
            raise err.ValidationError(*(e, 400))
        response = Response({"message": book_constants.STATUS_UPDATED}, status=status.HTTP_200_OK)
        return response


class BookReportView(ListAPIView):
    """
    Model view to generate the report
    """
    permission_classes = (IsLibraryStaff,)
    serializer_class = BookListSerializer

    def get(self, request):
        books_list = Book.objects.filter(status='borrowed')
        report_name = self.request.GET.get('report_name')
        generate_report(books_list, report_name)
        return Response({"message": book_constants.REPORT_GENERATED}, status=status.HTTP_200_OK)


class BookAmazonUpdateView(UpdateAPIView):
    """
    Model view to insert or update amazon id
    """
    serializer_class = BookAmazonUpdateSerializer
    permission_classes = (IsLibraryStaff, )

    def update(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        books = Book.objects.all()
        for book_instance in books:
            #: get the current amazon id of book
            current_amazon_id = book_instance.amazon_id
            #: Get the isbn of book
            isbn = book_instance.isbn
            #: Initialise it to existing for checking
            amazon_id = current_amazon_id
            try:
                api_response = requests.get(settings.OPEN_LIBRARY_URL+isbn)
                if api_response.status_code ==200:
                    amazon_id = json.loads(api_response.text).get('ISBN:'+isbn).get('identifiers').get('amazon')[0]
            except:
                #: There may be instances where there is no response
                pass
                #: Perform the update only if there is a difference in existing and the new
            if current_amazon_id != amazon_id:
                request.data['amazon_id'] = amazon_id
                serializer = self.get_serializer(book_instance, data=request.data, partial=True)
                try:
                    if serializer.is_valid(raise_exception=True):
                        self.perform_update(serializer)
                except Exception as e:
                    logger.error("Error inside post function inside BookAmazonUpdateView class. ERROR {}".format(str(e)))
                    raise err.ValidationError(*(e, 400))
        response = Response({"message": book_constants.AMAZON_UPDATED}, status=status.HTTP_200_OK)
        return response
