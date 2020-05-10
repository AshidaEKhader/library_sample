import logging
import re

from books import errors as err
from books import constants as const
from .models import Book, User

# Initialize logger
logger = logging.getLogger(__name__)


def validate_book_exists_based_on_id(book_id):
    """
    Function that returns Book instance if a book exists with the passed uid, else raises error.

    :param book_id: Book uid

    :return: Book Instance if the book does not exists else raise error
    """

    try:
        book_instance = Book.objects.get(id=book_id)

    except Exception as e:
        logger.error('Error inside validate_user_exists_based_on_uid function. ERROR: {}'.format(str(e)))
        raise err.NotFound(const.BOOK_NOT_FOUND, 404)

    return book_instance


def validate_books_status(book_instance):
    """
        Function that returns True if the book status is unavailable else raises error.

        :param book_instance: Book object

        :return:True if available else false
        """
    if book_instance.status == 'borrowed':
        return True
    return False

def validate_user_exists_based_on_uid(user_uid):
    """
        Function that returns User instance if a user exists with the passed uid, else raises error.

        :param user_uid: User uid

        :return: User Instance if the user does not exists else raise error
        """

    try:
        user_instance = User.objects.get(uid=user_uid)

    except Exception as e:
        logger.error('Error inside validate_user_exists_based_on_uid function. ERROR: {}'.format(str(e)))
        raise err.NotFound(const.USER_NOT_FOUND, 404)

    return user_instance


def check_book_exist_in_wishlist(book_instance, user_instace):
    """
    Finction to check whether a book is in the user's wish list
    :param book_instance:
    :param user_instace:
    :return: True if exist else false
    """
    wishlisted_books = user_instace.wishlist.all()
    if book_instance in wishlisted_books:
        return True
    return False